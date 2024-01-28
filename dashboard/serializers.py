from rest_framework import serializers
from doctors.models import MedicalTest, MedicalTestImage, Image




class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'



class MedicalTestImageSerializer(serializers.ModelSerializer):
    medical_test_images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = MedicalTestImage
        fields = '__all__'



class MedicalTestSerializer(serializers.ModelSerializer):
    test_images = MedicalTestImageSerializer(many=True, read_only=True)

    class Meta:
        model = MedicalTest
        fields = '__all__'
