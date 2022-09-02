FROM tensorflow/serving

COPY /img_classifier /models/img_classifier/1
ENV MODEL_NAME="img_classifier"