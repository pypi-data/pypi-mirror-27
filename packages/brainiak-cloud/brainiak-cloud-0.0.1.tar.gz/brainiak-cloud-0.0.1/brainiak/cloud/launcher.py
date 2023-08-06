import pickle

import nibabel
import numpy as np
import pika

from .consumer import Consumer

from brainiak.searchlight.searchlight import Searchlight, Diamond


def test_models(X, mask, radius, broadcast):
    classifier = pickle.loads(X[1][radius, radius, radius, 0])
    X_classifier = X[0][mask].T
    classes = classifier.predict(X_classifier)
    return classes[0]


def predict(sample, models, mask):
    test_searchlight = Searchlight(sl_rad=2, shape=Diamond)
    test_searchlight.distribute([sample, models[..., np.newaxis]], mask)
    test_classes = test_searchlight.run_searchlight(test_models)
    test_display = np.empty(test_classes.shape, dtype=float)
    test_display[test_classes == "face"] = 0.5
    test_display[test_classes == "house"] = 1
    test_display[test_classes == None] = np.nan
    return test_display


class Launcher:
    def __init__(self, work_queue, result_queue, experiment_data=None):
        # NOTE: We used to only have one channel; now we have one for
        # both of consumer and producer
        self.rmq = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.rmq.channel()
        self.channel.queue_declare(queue=work_queue)
        self.channel.queue_declare(queue=result_queue)
        models = experiment_data["models"]
        mask = experiment_data["mask_data"]
        affine = experiment_data["mask_affine"]

        self.counter = 0

        def callback(channel, method, properties, body):
            print('Received message %d!' % self.counter)
            self.counter += 1

            test_display = predict(pickle.loads(body), models, mask)
            test_img = nibabel.nifti1.Nifti1Image(test_display, affine)
            self.channel.basic_publish(
                exchange='',
                routing_key=result_queue,
                body=pickle.dumps(test_img),
            )
            return

        consumer = Consumer(
            'amqp://guest:guest@localhost:5672/%2F',
            routing_key=work_queue,
            callback=callback
        )
        consumer.run()
        #  self.channel.basic_consume(callback, queue=work_queue, no_ack=True)
        #  self.channel.start_consuming()
