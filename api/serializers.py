from rest_framework import serializers

from .models import Applicant

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = "__all__"
        read_only_fields = ["slug","uid","id",'app_enum_status','app_status']


# class UpdateApplicantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Applicant
#         fields = "__all__"






class ApplicantSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = (
            "first_name",
            "middle_name",
            "last_name",
            "age",
            # "get_profile_url",
            "get_resume",
            "get_cover_letter",
            "uid"
        )


class ApplicantStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = (
            "app_enum_status",
        )
        read_only_fields = ["slug","uid","id"]