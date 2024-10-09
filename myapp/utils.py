# image_bytes = query({"inputs": title})
            
#             # Save the image to the media directory
#             image = Image.open(io.BytesIO(image_bytes))
#             image_format = image.format.lower()  # Get the image format (e.g., png, jpg)
#             image_name = f"{title}.{image_format}"
#             image_path = default_storage.save(f'summaries/{image_name}', ContentFile(image_bytes))

#             # Create the summary object
#             Summary.objects.create(title=title, summary=summary, image=image_path)
#             serializer = SummarySerializer(Summary.objects.all(), many=True)
#             return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
#         return Response({"Error": "Some Error"}, status=status.HTTP_400_BAD_REQUEST)