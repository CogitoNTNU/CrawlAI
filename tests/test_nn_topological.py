import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model

from src.agent_parts.rectangle import Point
from src.agent import Agent

class MockAgent(Agent):
     def act(self, env) -> int:
          return 0


def test_do_inference_with_correct_input():
    
    agent = Agent()
    
    input_data = tf.random.uniform((1, input_size)) 
    x = [alpha1, 
         alpha2, 
         viewPos1, 
         viewPos2, 
         limbPos, 
         joint_angle, 
         health
         ]
    model = None

    output = model.predict(x)
    assert output is not None



def test_kill_neuron():
    # Remember to test if the connection is put on the correct place. 
    pass

def test_add_neuron():

    pass

def test_connection():

    pass

def test_add_connection():
    
    pass

def test_remove_connection():
    pass
    







