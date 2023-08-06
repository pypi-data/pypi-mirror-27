import pyconrad

_ = pyconrad.ClassGetter(
    'edu.stanford.rsl.conrad.utils',
    'java.beans',
    'java.io',
    'edu.stanford.rsl.conrad.geometry.trajectories'
)


def get_conf() -> pyconrad.AutoCompleteConrad.edu.stanford.rsl.conrad.utils.Configuration:
    conf = _.Configuration.getGlobalConfiguration()

    return conf


def get_geometry() -> pyconrad.AutoCompleteConrad.edu.stanford.rsl.conrad.geometry.trajectories.Trajectory:
    #  #TODO load config on pyconrad startup
    geo = _.Configuration.getGlobalConfiguration().getGeometry()
    return geo


def get_sino_shape() -> tuple:
    conf = _.Configuration.getGlobalConfiguration()
    geo = conf.getGeometry()
    return (geo.getProjectionStackSize(), geo.getDetectorHeight(), geo.getDetectorWidth())


def get_sino_size() -> list:
    return (reversed(get_sino_shape()))


def get_reco_shape() -> tuple:
    conf = _.Configuration.getGlobalConfiguration()
    geo = conf.getGeometry()  # type: AutoCompleteConrad.edu.stanford.rsl
    return (geo.getReconDimensionZ(), geo.getReconDimensionY(), geo.getReconDimensionX())


def get_reco_size() -> list:
    return (reversed(get_reco_shape()))
