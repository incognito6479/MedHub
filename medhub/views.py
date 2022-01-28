from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from medhub.models import Interrogator, Responder, Poll, Question, Token, Answer
from medhub.serializers import InterrogatorSerializer, PollSerializer
from medhub.helpers import get_tokens_for_user


class LoginApiView(APIView):
	# permission_classes = []

	def get(self, request):
		interrogators = Interrogator.objects.all()
		serializer = InterrogatorSerializer(data=interrogators, many=True)
		serializer.is_valid()
		context = {
			'interrogators': serializer.data
		}
		return Response(context)

	def post(self, request):
		username = self.request.data.get('username', None)
		password = self.request.data.get('password', None)

		if (username is None) or (password is None):
			context = {
				'msg': 'username or password is missing'
			}
			return Response(context)

		user = Interrogator.objects.filter(username=username).first()

		if user is None:
			context = {
				'msg': 'User is not found'
			}
			return Response(context)

		if (not user.check_password(password)):
			context = {
				'msg': 'password is incorrect'
			}
			return Response(context)

		resp = get_tokens_for_user(user)

		obj, created = Token.objects.get_or_create(
							user_id=user.id,
							defaults = {
								'token': resp['access']
							}
						)
		if not created:
			obj.token = resp['access']
			obj.save()

		context = {
			'msg': 'Login success',
			'token': resp['access']
		}
		return Response(context)


class PollApiView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		polls = Poll.objects.all().prefetch_related('questions')
		serializer = PollSerializer(data=polls, many=True)
		serializer.is_valid()
		context = {
			'polls': serializer.data
		}
		return Response(context)

	def post(self, request):
		if 'answer' in self.request.session:
			sub_answer = self.request.data.get('sub_answer', None)
			if (sub_answer is None) or (sub_answer == ""):
				context = {
					'msg': 'Please send the sub_answer'
				}
				return Response(context)
			# print(self.request.session['answer'])
			responder = Responder.objects.create(
							gender=self.request.session['answer']['gender'],
							birth_date=self.request.session['answer']['birth_date']
						)
			answer = Answer.objects.create(
							responder_id=responder.id,
							poll_id=self.request.session['answer']['poll_id'],
							interrogator_id=self.request.session['answer']['user_id'],
							main_answer=self.request.session['answer']['main_answer'],
							sub_answer=sub_answer
						)
			del self.request.session['answer']
			self.request.session.modified = True
			context = {
				'msg': 'Thanks for your answer'
			}
			return Response(context)

		poll_id = self.request.data.get('poll_id', None)
		question_id = self.request.data.get('question_id', None)
		main_answer = self.request.data.get('main_answer', None)
		birth_date = self.request.data.get('birth_date', None)
		gender = self.request.data.get('gender', None)

		if (poll_id is None) or (poll_id == "") or \
			(question_id is None) or (question_id == "") or \
			(main_answer is None) or (main_answer == "") or \
			(birth_date is None) or (birth_date == "") or \
			(gender is None) or (gender == ""):
			context = {
				'msg': 'Please send poll_id/question_id/main_answer/gender/birth_date to start answering the questions'
			}
			return Response(context)

		poll_obj = Poll.objects.filter(id=poll_id).first()
		question_obj = Question.objects.filter(id=question_id).first()

		if (poll_obj is None) or (question_obj is None):
			context = {
				'msg': 'poll_id/question_id is incorrect'
			}
			return Response(context)

		token_key = self.request.META.get('HTTP_AUTHORIZATION').split(' ')[1]

		token = Token.objects.filter(token=token_key).first()

		if (main_answer == 'Yes') or (main_answer == 'yes'):
			self.request.session['answer'] = {
				'poll_id': poll_id,
				'question_id': question_id,
				'user_id': token.user_id,
				'birth_date': birth_date,
				'gender': gender,
				'main_answer': main_answer
			}
			context = {
				'msg': f'Ok, now send the sub_answer for {question_obj.sub_question}'
			}
			return Response(context)
		else:
			responder = Responder.objects.create(
							gender=gender,
							birth_date=birth_date
						)
			answer = Answer.objects.create(
							responder_id=responder.id,
							poll_id=poll_id,
							interrogator_id=token.user_id,
							main_answer=main_answer
						)
			context = {
				'msg': 'Thanks for your answer'
			}
			return Response(context)

		context = {
			'msg': 'success',
			'token': token_key,
		}
		return Response(context)