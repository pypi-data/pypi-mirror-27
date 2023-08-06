#!/usr/bin/env python3
# system modules
import logging
import datetime
import textwrap
import collections
import itertools

# internal modules
from .genericmodel import GenericModel
from . import interfaces
from . import numericalschemes
from . import utils

# external modules
import numpy as np
import scipy.optimize

logger = logging.getLogger(__name__)

class NumericalModel(GenericModel):
    """
    Class for numerical models

    Args:
        name (str, optional): the model name
        version (str, optional): the model version
        description (str): a short model description
        long_description (str): an extended model description
        authors (:any:`str`, :any:`list` or :any:`dict`, optional):
            the model author(s). One of

            :any:`str`:
                name of single author
            :any:`list` of :any:`str`:
                :any:`list` of author names
            :any:`dict`:
                :any:`dict` of ``{'task': ['name1','name1']}`` pairs
        initial_time (float): initial model time (UTC unix timestamp)
        observations (SetOfObservations, optional): observations
        parameters (SetOfParameters, optional): model parameters
        forcing (SetOfForcingValues, optional): model forcing
        variables (SetOfStateVariables, optional): model state variables
        numericalschemes (SetOfNumericalSchemes, optional): model schemes with
            equation
    """
    def __init__(self,
            name = None,
            version = None,
            description = None,
            long_description = None,
            authors = None,
            initial_time = None,
            parameters = None,
            observations = None,
            forcing = None,
            variables = None,
            numericalschemes = None,
            ):
        # GenericModel constructor
        GenericModel.__init__(self,
            name = name,
            version = version,
            description = description,
            long_description = long_description,
            authors = authors,
            )

        self.logger = logging.getLogger(__name__) # logger

        # set properties
        if not initial_time is None:
            self.initial_time = initial_time
        if not parameters is None:
            self.parameters = parameters
        if not forcing is None:
            self.forcing = forcing
        if not observations is None:
            self.observations = observations
        if not variables is None:
            self.variables = variables
        if not numericalschemes is None:
            self.numericalschemes = numericalschemes

    ##################
    ### Properties ###
    ##################
    @property
    def initial_time(self):
        """
        The initial model time

        :type: :any:`float`
        """
        try:                   self._initial_time
        except AttributeError: self._initial_time = self._default_initial_time
        return self._initial_time

    @initial_time.setter
    def initial_time(self,newtime):
        assert utils.is_numeric(newtime), "initial_time has to be numeric"
        assert np.array(newtime).size == 1, "initial_time has to be one value"
        self._initial_time = newtime

    @property
    def _default_initial_time(self):
        """
        Default initial model time if none was given

        :type: :any:`float`
        """
        return utils.utcnow()

    @property
    def _default_name(self):
        """
        Default name if none was given

        :type: :any:`str`
        """
        return "numerical model"

    @property
    def _default_description(self):
        """
        Default description if none was given

        :type: :any:`str`
        """
        return "a numerical model"

    @property
    def _default_long_description(self):
        """
        Default long_description if none was given

        :type: :any:`str`
        """
        return "This is a numerical model."

    @property
    def observations(self):
        """
        The model observations

        :type: :any:`SetOfObservations`
        """
        try:                   self._observations # already defined?
        except AttributeError: self._observations = self._default_observations
        return self._observations # return

    @observations.setter
    def observations(self,newobservations):
        assert issubclass(newobservations.__class__,
            interfaces.SetOfObservations),\
            "observations has to be object of subclass of SetOfObservations"
        self._observations = newobservations
        self._observations.time_function = self.get_model_time # time function

    @property
    def _default_observations(self):
        """
        Default observations if none were given

        :type: :any:`SetOfObservations`
        """
        return interfaces.SetOfObservations()

    @property
    def parameters(self):
        """
        The model parameters

        :type: :any:`SetOfParameters`
        """
        try:                   self._parameters # already defined?
        except AttributeError: self._parameters = self._default_parameters
        return self._parameters # return

    @parameters.setter
    def parameters(self,newparameters):
        assert issubclass(newparameters.__class__, interfaces.SetOfParameters),\
            "parameters has to be object of subclass of SetOfParameters"
        self._parameters = newparameters
        self._parameters.time_function = self.get_model_time # set time function

    @property
    def _default_parameters(self):
        """
        Default parameters if none were given

        :type: :any:`SetOfParameters`
        """
        return interfaces.SetOfParameters()

    @property
    def forcing(self):
        """
        The model forcing

        :type: :any:`SetOfForcingValues`
        """
        try:                   self._forcing # already defined?
        except AttributeError: self._forcing = self._default_forcing
        return self._forcing # return

    @forcing.setter
    def forcing(self,newforcing):
        assert issubclass(newforcing.__class__, interfaces.SetOfForcingValues),\
            "forcing has to be object of subclass of SetOfForcingValues"
        self._forcing = newforcing
        self._forcing.time_function = self.get_model_time # set time function

    @property
    def _default_forcing(self):
        """
        Default forcing if none was given

        :type: :any:`SetOfForcingValues`
        """
        return interfaces.SetOfForcingValues()

    @property
    def variables(self):
        """
        The model variables

        :type: :any:`SetOfStateVariables`
        """
        try:                   self._variables # already defined?
        except AttributeError: # default
            self._variables = interfaces.SetOfStateVariables()
        return self._variables # return

    @variables.setter
    def variables(self,newvariables):
        assert issubclass(newvariables.__class__,
            interfaces.SetOfStateVariables), \
            "variables has to be object of subclass of SetOfStateVariables"
        self._variables = newvariables
        self._variables.time_function = self.get_model_time # set time function

    @property
    def _default_variables(self):
        """
        Default variables if none were given

        :type: :any:`SetOfStateVariables`
        """
        return interfaces.SetOfStateVariables()

    @property
    def numericalschemes(self):
        """
        The model numerical schemes

        :type: :any:`str`
        """
        try:                   self._numericalschemes # already defined?
        except AttributeError: self._numericalschemes = self._default_numericalschemes
        return self._numericalschemes # return

    @numericalschemes.setter
    def numericalschemes(self,newnumericalschemes):
        assert isinstance(newnumericalschemes,
            numericalschemes.SetOfNumericalSchemes),\
            "numericalschemes has to be instance of SetOfNumericalSchemes"
        self._numericalschemes = newnumericalschemes

    @property
    def _default_numericalschemes(self):
        """
        Default numerical schemes if none were given

        :type: :any:`SetOfNumericalSchemes`
        """
        return numericalschemes.SetOfNumericalSchemes()


    @property
    def model_time(self):
        """
        The current model time

        :type: :any:`float`
        """
        try:                   self._model_time # already defined?
        except AttributeError: self._model_time = self.initial_time # default
        return float(self._model_time) # return

    @model_time.setter
    def model_time(self, newtime):
        assert utils.is_numeric(newtime), "model_time has to be numeric"
        assert np.array(newtime).size == 1, "model_time has to be one value"
        self._model_time = float(newtime)

    ###############
    ### Methods ###
    ###############
    def get_model_time(self):
        """
        The current model time

        Returns:
            float: current model time
        """
        return self.model_time

    def integrate(self, final_time = None, seconds = None):
        """
        Integrate the model until final_time

        Args:
            final_time (float): time to integrate until. Conflicts with
                ``seconds``.
            seconds (float): seconds to integrate. Conflicts with
                ``final_time``.
        """
        self.logger.info("start integration")
        if not final_time is None and seconds is None:
            pass
        elif final_time is None and not seconds is None:
            final_time = self.model_time + seconds
        else:
            raise ValueError("Specify either 'final_time' or 'seconds'")
        self.numericalschemes.integrate(
            start_time = self.model_time,
            final_time = final_time,
            )
        self.model_time = final_time
        self.logger.info("end of integration")

    def optimize(self, bring_together, variate, time_start = None,
        time_end = None, **kwargs):
        """
        Optimize the :any:`InterfaceValue` s in ``variate`` such that the
        :any:`InterfaceValue` s in ``bring_together`` fit best.

        .. note::

            This method repeatedly **deletes** the data in the given time span
            and simulates it again with slightly modified input.

        Args:
            bring_together (list): The :any:`InterfaceValue` s to bring
                together. This is a :any:`list` like
                ``[[InterfaceValue(),...],[InterfaceValue(),...]]``.
            variate (dict): The :any:`InterfaceValue` s to variate and optimize.
                This is a :any:`dict` like
                ``variate[InterfaceValue()]=n_blocks`` where ``n_blocks`` is an
                :any:`int` specifying how many blocks are used across the time
                span to optimize this :any:`InterfaceValue`. Use ``1`` to
                optimize a constant (e.g. a :any:`Parameter` that doesn't change
                in time) and greater values for temporally variable values.
            time_start (float, optional): The time to start optimizing. Defaults
                to the earliest variable time in ``variate``.
            time_end (float, optional): The time to end optimizing. Defaults
                to the :any:`model_time`

        Kwargs:
            kwargs (dict, optional): further arguments passed to
            :any:`scipy.optimize.minimize`. ``method`` defaults to
            ``L-BFGS-B``.

        Returns:
            optimization result
        """
        minimize_kwargs = {"method":"L-BFGS-B"}
        minimize_kwargs.update(kwargs)
        # fix order of values to optimize
        variate = collections.OrderedDict(variate)
        for iv,nblocks in variate.items():
            assert nblocks > 0

        # determine time range to use
        if time_start is None:
            time_start = min([min(iv.times) for iv in variate.keys()])
        if time_end is None:
            time_end = self.model_time
        assert time_end > time_start

        # residual function
        def residual(state, *args):
            # check input for bounds
            for i,v in enumerate(state):
                lower, upper = bounds[i]
                if state[i] < lower:
                    logger.warning("scipy.optimize.minimize specified a value "
                        "smaller than the lower bound ({} > {})".format(
                        state[i],lower))
                    state[i] = max(state[i],lower)
                elif state[i] > upper:
                    logger.warning("scipy.optimize.minimize specified a value "
                        "greater than the upper bound ({} > {})".format(
                        state[i],upper))
                    state[i] = min(state[i],upper)

            # clear the time span
            for iv in itertools.chain(variate.keys(),self.variables.elements):
                iv.cut(end = time_start)

            # reset model time
            self.model_time = time_start

            # set new state
            stateiter = iter(state)
            newstate = []
            for iv,nblocks in variate.items():
                iv.merge_accumulated()
                iv_newstate = []
                for i in range(nblocks):
                    iv_newstate.append(next(stateiter))
                newstate.append(iv_newstate)
            for iv,data in zip(variate.keys(),newstate):
                times = np.linspace(time_start,time_end,len(data))
                iv[slice(time_start,time_end)] = (times,data)

            # simulate
            self.integrate(final_time = time_end)

            # calculate residual
            res = 0

            for ivlist in bring_together:
                times = np.unique(np.concatenate(
                    [iv[slice(time_start,time_end)][0] for iv in ivlist]))
                res += utils.multi_rmse(*[iv(times) for iv in ivlist])

            logger.debug("residual is {}".format(res))

            return res

        # first guess is current model state
        first_guess = []
        for iv,nblocks in variate.items():
            first_guess.extend(
                iv(np.linspace(time_start,time_end,nblocks)).flatten())
        logger.debug("first_guess: {}".format(first_guess))

        # get bounds
        bounds = []
        for iv,nblocks in variate.items():
            bounds.extend([iv.bounds]*nblocks)
        logger.debug("bounds: {}".format(bounds))

        # optimize
        result = scipy.optimize.minimize(
            fun = residual,
            x0 = first_guess,
            bounds = bounds,
            **kwargs
            )

        logger.debug("Optimization result:\n{}".format(result))

        return result

    def gui(self, *args, **kwargs): # pragma: no cover
        """
        Open a GTK window to interactively run the model:

        - change the model variables, parameters and forcing on the fly
        - directly see the model output
        - stepwise integration

        Args:
            args, kwargs : arguments passed to :any:`NumericalModelGui`
        """
        from .gui import NumericalModelGui
        # create a gui
        gui = NumericalModelGui( numericalmodel = self,
            *args, **kwargs)
        # run the gui
        gui.run()

    def __str__(self): # pragma: no cover
        """
        Stringification

        Returns:
            str : a summary
        """
        # GenericModel stringificator
        gm_string = GenericModel.__str__(self)

        string = textwrap.dedent(
            """
            {gm_string}

            ##################
            ### Model data ###
            ##################

            initial time: {initialtime}

            #################
            ### Variables ###
            #################

            {variables}

            ##################
            ### Parameters ###
            ##################

            {parameters}

            ###############
            ### Forcing ###
            ###############

            {forcing}

            ####################
            ### Observations ###
            ####################

            {observations}

            ###############
            ### Schemes ###
            ###############

            {schemes}

            """
            ).strip().format(
            initialtime = self.initial_time,
            gm_string = gm_string,
            parameters = self.parameters,
            variables = self.variables,
            forcing = self.forcing,
            schemes = self.numericalschemes,
            observations = self.observations,
            )

        return string
