'''
Importing necessary modeuls
'''
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView,
    RetrieveDestroyAPIView,
    ListAPIView
)

from rest_framework import filters

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination

from rest_framework.decorators import api_view
from django.db.models import Q
from django.http import Http404

from drf_yasg.utils import swagger_auto_schema

from .serializers import ApplicantSerializer, ApplicantSerializerV2, ApplicantStatusSerializer

from .models import Applicant


#############################################################################
# ONLY THE CREATEVIEW AND RETRIEVE-UPDATE-DESTROY API ARE SUFFICIENT FOR THE CRUD OPERATIONS
# FOR THE SAKE OF THIS EXERCISE, EXTRA GENERIC API VIEWS ARE USER.
#############################################################################
######################### CRUD Opertaions ###################################
#############################################################################

# Using DRF Generic to inhereit and extend CRUD OPerations.


class ApplicantCreateView(CreateAPIView):
    '''
    This class helps in creating an aplicant.
    Swagger -> create -> 2 methods: get and post.
    '''
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    # permission_classes = (permissions.IsAuthenticated, )
#############################################################################


class ApplicantGetUpateDeleteView(RetrieveUpdateDestroyAPIView):
    '''
    This class retrieves, updates and deletes as required.
    Swagger -> profile -> get, put, pathch and delete methods.
    '''
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    lookup_field = 'uid'

#############################################################################
# THE ABOVE TWO APIs SATSIFY THE CRUD REQUIREMENTS.
# THE BELOW APIs ARE FOR SAKE OF DEMONSTRATION.

#############################################################################

class ApplicantDetailsView(RetrieveAPIView):
    '''
    This class retrieves an individual applicant's profile
    Swagger -> details -> get method(V1).
    '''
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    lookup_field = 'uid'
    # permission_classes = (permissions.AllowAny, )
#############################################################################


class ApplicantUpdateView(RetrieveUpdateAPIView):
    '''
    This class retrives the applicants profile and updates the needed.
    Swagger -> update -> get, put and patch method.
    '''
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    lookup_field = 'uid'
#############################################################################


class ApplicantDeleteView(RetrieveDestroyAPIView):
    '''
    This class retrieves and deletes as needed.
    Swagger -> delete -> get and delete method.
    '''
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    lookup_field = 'uid'
#############################################################################
######################### Search And Filtering ##############################
#############################################################################

class Paginator(PageNumberPagination):
    '''
    Creating a sub class for pagination.
    Structurally this code would be include in it's own file/module for resuability.
    '''
    page_size = 3
    page_query_param = "pg_no"
    page_size_query_param = 'records'
    max_page_size = 5


class ApplicantSearchView(ListAPIView):
    '''
    This method is used to search/filter and retreieve a list of applications.
    Swagger -> search -> get
    '''
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = Paginator
    search_fields = ["uid", "app_enum_status",
                     "app_status", "first_name", "last_name"]

# Method2


@swagger_auto_schema(method='post', request_body=ApplicantSerializerV2)
@api_view(['POST'])
def search(request):
    '''
    This is an alternate method to search/ filter for applicants.
    Form data is to be submitted as json with key as "query"
    Example: {
        "query": "123456"
    }
    The value of the 'query' can be first_name(John/john), uid(13456),
        application status(True/False/true/false), or app_enm status(Rejected/Pending/Accepted)
    Swagger -> search -> post method.
    '''
    query = request.data.get('query', '')
    if query:
        products = Applicant.objects.filter(Q(
            uid__icontains=query) | Q(first_name__icontains=query) | Q(
            app_enum_status__icontains=query) | Q(app_status__icontains=query))
        serializer = ApplicantSerializerV2(products, many=True)
        return Response(serializer.data)
    return Response({"applicants": []})


############################################################################
####################### Accepting or Rejecting an application ##############
############################################################################


class ApplicantStatus(RetrieveUpdateAPIView):
    '''
    This class is used to accept or reject and application.
    The class works by altering the enum status of the record.
    ''' 
    queryset = Applicant.objects.all()
    serializer_class = ApplicantStatusSerializer
    lookup_field = 'uid'

    def partial_update(self, request, *args, **kwargs):
        uid = int(kwargs['uid'])
        applicant= Applicant.objects.get(uid=uid)
        applicant.app_enum_status = (request.data['app_enum_status'])
        try:
            applicant.check_app_status_bool()
        except Exception as keyerror:
        # print(keyerror) 
            return Response(
                {
                "error": "Key Error",
                "message": f"Entered Key is {keyerror}. Allowed keys are '2' for pending, '1' for accepted and '0' for rejected"
                }
                )
        return super().partial_update(request, *args, **kwargs)

############################################################################
############################# Extra Stuff ##################################
############################################################################


class ApplicantDetailsViewV2(APIView):
    '''
    An alternate class to get details of applicants.
    Extends from the DRF's APIView.
    '''

    def get_object(self, uid):
        '''
        Custom method to retrieve the objects from the dB.
        '''
        try:
            return Applicant.objects.get(uid=uid)
        except Applicant.DoesNotExist:
            raise Http404

    def get(self, request, uid, format=None):
        '''
        Over writing the inbuilt get method.
        '''
        applicant = self.get_object(uid)
        serializer = ApplicantSerializerV2(applicant)
        return Response(serializer.data)
