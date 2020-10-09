from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic import View as GView

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from workflow.models import Program, Organization

from .forms import IndividualForm, HouseholdForm
from .models import Individual, Distribution, Training, Household

from .serializers import IndividualSerializer, HouseholdSerializer, HouseholdListDataSerializer


class IndividualView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Individual.objects.all()
    serializer_class = IndividualSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        organization = self.request.user.activity_user.organization
        get_programs = Program.objects.all().filter(organization=organization)
        queryset = Individual.objects.filter(program__in=get_programs)

        program_id = self.request.query_params.get('program', None)
        distribution_id = self.request.query_params.get('distribution', None)
        training_id = self.request.query_params.get('training', None)
        if program_id is not None:
            programs = Program.objects.filter(id=program_id)
            queryset = queryset.filter(program__in=programs)
        if distribution_id is not None:
            distributions = Distribution.objects.filter(id=distribution_id)
            queryset = queryset.filter(distribution__in=distributions)
        if training_id is not None:
            training = Training.objects.filter(id=training_id)
            queryset = queryset.filter(training__in=training)
        return queryset


class IndividualList(ListView):
    """
    Individual
    """
    model = Individual
    template_name = 'formlibrary/individual.html'

    def get(self, request, *args, **kwargs):

        program_id = self.kwargs['program']
        training_id = self.kwargs['training']
        distribution_id = self.kwargs['distribution']

        organization = request.user.activity_user.organization
        get_programs = Program.objects.all().filter(organization=organization)

        get_training = Training.objects.filter(
            program__in=get_programs)
        get_distribution = Distribution.objects.filter(
            program__in=get_programs)
        get_individuals = Individual.objects.filter(
            program__in=get_programs)

        if int(program_id) != 0:
            get_individuals = Individual.objects.filter(
                program__id__contains=program_id)
        if int(training_id) != 0:
            get_individuals = Individual.objects.filter(
                training__id=int(training_id))
        if int(distribution_id) != 0:
            get_individuals = Individual.objects.filter(
                distribution__id=int(distribution_id))

        return render(request, self.template_name,
                      {
                          'get_individuals': get_individuals,
                          'program_id': int(program_id),
                          'get_programs': get_programs,
                          'get_distribution': get_distribution,
                          'get_training': get_training,
                          'training_id': int(training_id),
                          'distribution_id': int(distribution_id),
                          'form_component': 'individual_list',
                          'active': ['forms', 'individual_list']
                      })


class IndividualUpdate(UpdateView):
    """
    Individual update
    """
    model = Individual
    template_name = 'formlibrary/individual_form.html'
    success_url = '/formlibrary/individual_list/0/0/0'
    form_class = IndividualForm

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(IndividualUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['organization'] = self.request.user.activity_user.organization
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(IndividualUpdate, self).get_context_data(**kwargs)
        context['current_program'] = self.get_object()
        context['active'] = ['formlibrary']
        return context


class GetIndividualData(GView):
    """
    View all individual data
    """
    def get(self, request):
        try:
            organization = request.user.activity_user.organization
            get_programs = Program.objects.all().filter(organization=organization)

            get_training = Training.objects.filter(
                program__in=get_programs).values()
            get_distribution = Distribution.objects.filter(
                program__in=get_programs).values()
            individuals = Individual.objects.all().filter(
                program__in=get_programs)
            get_individuals = IndividualSerializer(individuals, many=True)

            return JsonResponse(
                dict(
                    level_1_label=organization.level_1_label,
                    individual_label=organization.individual_label,
                    programs=list(get_programs.values()),
                    trainings=list(get_training),
                    distributions=list(get_distribution),
                    individuals=list(get_individuals.data), safe=False

                )
            )
        except Exception as e:
            return JsonResponse(dict(error=str(e)))


class HouseholdView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        organization = self.request.user.activity_user.organization
        request.data['organization'] = organization.id
        request.data['label'] = organization.household_label
        request.data['program'] = request.data['program'][0] if request.data['program'] else 0
        request.data['created_by'] = self.request.user.activity_user.id
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        organization = self.request.user.activity_user.organization.id
        return Household.objects.filter(organization=organization)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class HouseholdlList(ListView):
    """
    Individual
    """
    model = Individual
    template_name = 'formlibrary/household.html'

    def get(self, request, *args, **kwargs):

        organization = request.user.activity_user.organization
        get_households = Household.objects.all().filter(organization=organization)

        context = {
            'households': get_households,
            'form_component': 'household_list',
            'active': ['forms', 'household_list']
        }

        return render(request, self.template_name, context)


# def list_households(request):
#     user = ActivityUser.objects.filter(user=request.user).first()
#     households = Household.objects.filter(organization=user.organization)
#     context = {
#         'households': households,
#         'active': ['formlibrary']
#     }
#     return render(request, 'formlibrary/household.html', context)


class HouseholdDataView(ListCreateAPIView):

    serializer_class = HouseholdListDataSerializer
    """
    View to fetch all households
    """

    def get_queryset(self):
        organization = self.request.user.activity_user.organization.id
        return Household.objects.filter(organization=organization)

    def get(self, request, *args, **kwargs):
        organization = Organization.objects.get(id=request.user.activity_user.organization.id)
        programs = Program.objects.all().filter(organization=organization).values('id', 'name')

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        data = dict(
                household_label=organization.household_label,
                individual_label=organization.individual_label,
                households=list(serializer.data),
                programs=list(programs),
                safe=False
            )
        return JsonResponse(data)


class HouseholdUpdate(UpdateView):
    model = Household
    template_name = 'formlibrary/household_form.html'
    success_url = '/formlibrary/household_list'
    form_class = HouseholdForm

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(HouseholdUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['organization'] = self.request.user.activity_user.organization
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(HouseholdUpdate, self).get_context_data(**kwargs)
        context['current_household'] = self.get_object()
        context['active'] = ['formlibrary']
        return context
