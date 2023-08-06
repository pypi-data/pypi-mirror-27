import pyconrad.autoinit

_ = pyconrad.ClassGetter('edu.stanford.rsl.tutorial.cone')


# def test_init_cone_beam_backprojector():
#     """
#     CONRAD crashes on the creation of a OpenCL when using the CONRAD.jar version 1.0.7 on Linux
#     (Not only in pyconrad but also when executing the only jar).
#     This does not happen if you compile CONRAD from the repository
#     """
#     _.ConeBeamBackprojector()


# if __name__ == "__main__":
#     test_init_cone_beam_backprojector()
