from rest_framework import serializers
from medhub.models import Interrogator, Responder, Poll, Question, Answer
from django.db.models import Count


class QuestionsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = 'id', 'main_question', 'sub_question'


class PollSerializer(serializers.ModelSerializer):
	questions_obj = QuestionsSerializer(many=True, read_only=True, source="questions")

	class Meta:
		model = Poll
		fields = 'id', 'created', 'questions_obj'


class ResponderSerializer(serializers.ModelSerializer):
	poll_obj = PollSerializer(many=False, read_only=True, source="poll")

	class Meta:
		model = Responder
		fields = 'id', 'birth_date', 'gender', 'poll_obj'


class InterrogatorSerializer(serializers.ModelSerializer):
	responders_obj = ResponderSerializer(many=True, read_only=True, source="responders")
	responders_count = serializers.SerializerMethodField('interviewed_count')

	class Meta:
		model = Interrogator
		fields = 'id', 'username', 'full_name', 'responders_count', 'responders_obj'


	def interviewed_count(self, v):
		ans = Answer.objects.filter(interrogator_id=v.id).values('id').annotate(Count('interrogator'))
		if ans:
			ans = ans[0]['interrogator__count']
		return 0