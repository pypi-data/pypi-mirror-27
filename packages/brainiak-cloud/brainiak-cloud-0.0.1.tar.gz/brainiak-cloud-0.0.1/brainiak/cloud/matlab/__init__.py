import os
import matlab.engine

# TODO: Life would be easier if we used an existing MATLAB engine
# so we didn't have to restart MATLAB each time.
# https://www.mathworks.com/help/matlab/matlab_external/connect-python-to-running-matlab-session.html
engine = matlab.engine.start_matlab()
engine.cd(os.path.dirname(os.path.realpath(__file__)))
engine.triarea(nargout=0)
