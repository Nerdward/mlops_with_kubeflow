import kserve
from typing import Dict, List
from keras_image_helper import create_preprocessor
import logging
import io
import base64

logging.basicConfig(level=kserve.constants.KSERVE_LOGLEVEL)

# for REST predictor the preprocess handler converts to input dict to the v1 REST protocol dict
class ImageTransformer(kserve.Model):
    def __init__(self, name: str, predictor_host: str):
        super().__init__(name)
        self.predictor_host = predictor_host
        self.preprocessor = create_preprocessor('xception', target_size=(299, 299))
        self.classes = [
                        'dress',
                        'hat',
                        'longsleeve',
                        'outwear',
                        'pants',
                        'shirt',
                        'shoes',
                        'shorts',
                        'skirt',
                        't-shirt'
                    ]

    def prepare_inputs(self, url:List) -> List:
        X = self.preprocessor.from_url(url)
        return X[0].tolist()

    def preprocess(self, inputs: Dict) -> Dict:
        return {'instances': [self.prepare_inputs(instance) for instance in inputs['instances']]}

    def postprocess(self, inputs: Dict) -> Dict:
        result = []
        for prediction in inputs['predictions']:
            output = dict(zip(self.classes, prediction)) 
            result.append(output)

        return {"predictions": result}

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(parents=[kserve.model_server.parser])
    parser.add_argument("--predictor_host", help="The URL for the model predict function", required=True)
    parser.add_argument("--model_name", help="The name of the model", required=True)

    args, _ = parser.parse_known_args()

    model_name = args.model_name
    host = args.predictor_host

    transformer = ImageTransformer(model_name, predictor_host=host)

    kserve.ModelServer(workers=1).start([transformer])