from rest_framework import serializers
from formlibrary.models import Individual, Training, Distribution, Household
from workflow.serializers import SiteProfileSerializer, ProgramSerializer
from feed.serializers import ActivityUserSerializer


class TrainingSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(format="%Y-%m-%d", input_formats=['%Y-%m-%d', ])
    end_date = serializers.DateField(format="%Y-%m-%d", input_formats=['%Y-%m-%d', ])

    class Meta:
        model = Training
        fields = '__all__'


class TrainingListSerializer(serializers.ModelSerializer):
    program = ProgramSerializer()
    created_by = ActivityUserSerializer()

    class Meta:
        model = Training
        fields = ['id', 'name', 'created_by', 'create_date', 'program']


class DistributionSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(format="%Y-%m-%d", input_formats=['%Y-%m-%d', ])
    end_date = serializers.DateField(format="%Y-%m-%d", input_formats=['%Y-%m-%d', ])

    class Meta:
        model = Distribution
        fields = '__all__'


class DistributionListSerializer(serializers.ModelSerializer):
    program = ProgramSerializer()
    created_by = ActivityUserSerializer()

    class Meta:
        model = Distribution
        fields = ['id', 'name', 'created_by', 'create_date', 'program']


class IndividualSerializer(serializers.ModelSerializer):
    training = TrainingSerializer(many=True, read_only=True)
    distribution = DistributionSerializer(many=True, read_only=True)
    site = SiteProfileSerializer(read_only=True)
    program = ProgramSerializer

    class Meta:
        model = Individual
        fields = ['id', 'first_name', 'last_name', 'id_number', 'primary_phone',
                  'date_of_birth', 'sex', 'age',
                  'training', 'distribution', 'site', 'program', 'create_date']

        def get_age(self, obj):
            return obj.individual.age()


class HouseholdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Household
        exclude = ['postal_code']


class HouseholdListDataSerializer(serializers.ModelSerializer):
    program = ProgramSerializer()
    created_by = ActivityUserSerializer()

    class Meta:
        model = Household
        fields = ['id', 'name', 'duration', 'program', 'created_by', 'create_date']
