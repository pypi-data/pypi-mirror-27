# -*- coding: utf-8 -*-

# Automatically generated - don't edit.
# Use `python setup.py build_ui` to update it.

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Ridge_CV = QtWidgets.QGroupBox(self.groupBox)
        self.Ridge_CV.setObjectName("Ridge_CV")
        self.formLayout_6 = QtWidgets.QFormLayout(self.Ridge_CV)
        self.formLayout_6.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_6.setObjectName("formLayout_6")
        self.alphasLabel_cv = QtWidgets.QLabel(self.Ridge_CV)
        self.alphasLabel_cv.setObjectName("alphasLabel_cv")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.alphasLabel_cv)
        self.alphasLineEdit_cv = QtWidgets.QLineEdit(self.Ridge_CV)
        self.alphasLineEdit_cv.setObjectName("alphasLineEdit_cv")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.alphasLineEdit_cv)
        self.fitInterceptLabel_cv = QtWidgets.QLabel(self.Ridge_CV)
        self.fitInterceptLabel_cv.setObjectName("fitInterceptLabel_cv")
        self.formLayout_6.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.fitInterceptLabel_cv)
        self.fitInterceptCheckBox_cv = QtWidgets.QCheckBox(self.Ridge_CV)
        self.fitInterceptCheckBox_cv.setChecked(True)
        self.fitInterceptCheckBox_cv.setObjectName("fitInterceptCheckBox_cv")
        self.formLayout_6.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.fitInterceptCheckBox_cv)
        self.normalizeLabel_cv = QtWidgets.QLabel(self.Ridge_CV)
        self.normalizeLabel_cv.setObjectName("normalizeLabel_cv")
        self.formLayout_6.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.normalizeLabel_cv)
        self.normalizeCheckBox_cv = QtWidgets.QCheckBox(self.Ridge_CV)
        self.normalizeCheckBox_cv.setObjectName("normalizeCheckBox_cv")
        self.formLayout_6.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.normalizeCheckBox_cv)
        self.scoringLabel_cv = QtWidgets.QLabel(self.Ridge_CV)
        self.scoringLabel_cv.setObjectName("scoringLabel_cv")
        self.formLayout_6.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.scoringLabel_cv)
        self.scoringComboBox_cv = QtWidgets.QComboBox(self.Ridge_CV)
        self.scoringComboBox_cv.setObjectName("scoringComboBox_cv")
        self.scoringComboBox_cv.addItem("")
        self.scoringComboBox_cv.addItem("")
        self.scoringComboBox_cv.addItem("")
        self.formLayout_6.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.scoringComboBox_cv)
        self.gCVModeLabel_cv = QtWidgets.QLabel(self.Ridge_CV)
        self.gCVModeLabel_cv.setObjectName("gCVModeLabel_cv")
        self.formLayout_6.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.gCVModeLabel_cv)
        self.gCVModeComboBox_cv = QtWidgets.QComboBox(self.Ridge_CV)
        self.gCVModeComboBox_cv.setObjectName("gCVModeComboBox_cv")
        self.gCVModeComboBox_cv.addItem("")
        self.gCVModeComboBox_cv.addItem("")
        self.gCVModeComboBox_cv.addItem("")
        self.gCVModeComboBox_cv.addItem("")
        self.formLayout_6.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.gCVModeComboBox_cv)
        self.storeCVValuesLabel_cv = QtWidgets.QLabel(self.Ridge_CV)
        self.storeCVValuesLabel_cv.setObjectName("storeCVValuesLabel_cv")
        self.formLayout_6.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.storeCVValuesLabel_cv)
        self.storeCVValuesCheckBox_cv = QtWidgets.QCheckBox(self.Ridge_CV)
        self.storeCVValuesCheckBox_cv.setObjectName("storeCVValuesCheckBox_cv")
        self.formLayout_6.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.storeCVValuesCheckBox_cv)
        self.horizontalLayout.addWidget(self.Ridge_CV)
        self.Ridge = QtWidgets.QGroupBox(self.groupBox)
        self.Ridge.setEnabled(True)
        self.Ridge.setObjectName("Ridge")
        self.formLayout_2 = QtWidgets.QFormLayout(self.Ridge)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.alphaLabel = QtWidgets.QLabel(self.Ridge)
        self.alphaLabel.setObjectName("alphaLabel")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.alphaLabel)
        self.alphaDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.Ridge)
        self.alphaDoubleSpinBox.setProperty("value", 1.0)
        self.alphaDoubleSpinBox.setObjectName("alphaDoubleSpinBox")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.alphaDoubleSpinBox)
        self.copyXLabel = QtWidgets.QLabel(self.Ridge)
        self.copyXLabel.setObjectName("copyXLabel")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.copyXLabel)
        self.copyXCheckBox = QtWidgets.QCheckBox(self.Ridge)
        self.copyXCheckBox.setChecked(True)
        self.copyXCheckBox.setObjectName("copyXCheckBox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.copyXCheckBox)
        self.fitInterceptLabel = QtWidgets.QLabel(self.Ridge)
        self.fitInterceptLabel.setObjectName("fitInterceptLabel")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.fitInterceptLabel)
        self.fitInterceptCheckBox = QtWidgets.QCheckBox(self.Ridge)
        self.fitInterceptCheckBox.setChecked(True)
        self.fitInterceptCheckBox.setObjectName("fitInterceptCheckBox")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.fitInterceptCheckBox)
        self.maxNumOfIterationsLabel = QtWidgets.QLabel(self.Ridge)
        self.maxNumOfIterationsLabel.setObjectName("maxNumOfIterationsLabel")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.maxNumOfIterationsLabel)
        self.maxNumOfIterationslineEdit = QtWidgets.QLineEdit(self.Ridge)
        self.maxNumOfIterationslineEdit.setObjectName("maxNumOfIterationslineEdit")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.maxNumOfIterationslineEdit)
        self.normalizeLabel = QtWidgets.QLabel(self.Ridge)
        self.normalizeLabel.setObjectName("normalizeLabel")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.normalizeLabel)
        self.normalizeCheckBox = QtWidgets.QCheckBox(self.Ridge)
        self.normalizeCheckBox.setObjectName("normalizeCheckBox")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.normalizeCheckBox)
        self.solverLabel = QtWidgets.QLabel(self.Ridge)
        self.solverLabel.setObjectName("solverLabel")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.solverLabel)
        self.toleranceLabel = QtWidgets.QLabel(self.Ridge)
        self.toleranceLabel.setObjectName("toleranceLabel")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.toleranceLabel)
        self.toleranceDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.Ridge)
        self.toleranceDoubleSpinBox.setObjectName("toleranceDoubleSpinBox")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.toleranceDoubleSpinBox)
        self.randomStateLabel = QtWidgets.QLabel(self.Ridge)
        self.randomStateLabel.setObjectName("randomStateLabel")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.randomStateLabel)
        self.randomStateLineEdit = QtWidgets.QLineEdit(self.Ridge)
        self.randomStateLineEdit.setObjectName("randomStateLineEdit")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.randomStateLineEdit)
        self.solverComboBox = QtWidgets.QComboBox(self.Ridge)
        self.solverComboBox.setObjectName("solverComboBox")
        self.solverComboBox.addItem("")
        self.solverComboBox.addItem("")
        self.solverComboBox.addItem("")
        self.solverComboBox.addItem("")
        self.solverComboBox.addItem("")
        self.solverComboBox.addItem("")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.solverComboBox)
        self.horizontalLayout.addWidget(self.Ridge)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.formGroupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.formGroupBox_2.setObjectName("formGroupBox_2")
        self.formLayout_5 = QtWidgets.QFormLayout(self.formGroupBox_2)
        self.formLayout_5.setObjectName("formLayout_5")
        self.crossValidateLabel = QtWidgets.QLabel(self.formGroupBox_2)
        self.crossValidateLabel.setObjectName("crossValidateLabel")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.crossValidateLabel)
        self.crossValidateCheckBox = QtWidgets.QCheckBox(self.formGroupBox_2)
        self.crossValidateCheckBox.setChecked(True)
        self.crossValidateCheckBox.setObjectName("crossValidateCheckBox")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.crossValidateCheckBox)
        self.verticalLayout.addWidget(self.formGroupBox_2)
        self.verticalLayout_2.addWidget(self.groupBox)

        self.retranslateUi(Form)
        self.crossValidateCheckBox.toggled['bool'].connect(self.Ridge_CV.setVisible)
        self.crossValidateCheckBox.toggled['bool'].connect(self.Ridge.setHidden)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(("Form"))
        self.Ridge_CV.setTitle(("Ridge CV"))
        self.alphasLabel_cv.setText(("alphas"))
        self.alphasLineEdit_cv.setWhatsThis(("http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html"))
        self.alphasLineEdit_cv.setText(("0.1, 1.0, 10.0"))
        self.fitInterceptLabel_cv.setText(("Fit intercept "))
        self.fitInterceptCheckBox_cv.setToolTip(_translate("Form", "Whether to calculate the intercept for this model. If set to false,\n"
"no intercept will be used in calculations (e.g. data is expected to\n"
"be already centered)."))
        self.fitInterceptCheckBox_cv.setWhatsThis(("http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html"))
        self.normalizeLabel_cv.setText(("Normalize "))
        self.normalizeCheckBox_cv.setToolTip(_translate("Form", "This parameter is ignored when fit_intercept is set to False. If True,\n"
"the regressors X will be normalized before regression by subtracting\n"
"the mean and dividing by the l2-norm. If you wish to standardize,\n"
"please use sklearn.preprocessing.StandardScaler before calling fit on\n"
"an estimator with normalize=False."))
        self.normalizeCheckBox_cv.setWhatsThis(("http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html"))
        self.scoringLabel_cv.setText(("Scoring"))
        self.scoringComboBox_cv.setWhatsThis(("http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html"))
        self.scoringComboBox_cv.setItemText(0, ("None"))
        self.scoringComboBox_cv.setItemText(1, ("string"))
        self.scoringComboBox_cv.setItemText(2, ("callable"))
        self.gCVModeLabel_cv.setText(("GCV mode"))
        self.gCVModeComboBox_cv.setWhatsThis(("http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html"))
        self.gCVModeComboBox_cv.setItemText(0, ("None"))
        self.gCVModeComboBox_cv.setItemText(1, ("auto"))
        self.gCVModeComboBox_cv.setItemText(2, ("svd"))
        self.gCVModeComboBox_cv.setItemText(3, ("eigen"))
        self.storeCVValuesLabel_cv.setText(("Store CV Values           "))
        self.storeCVValuesCheckBox_cv.setWhatsThis(("http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html"))
        self.Ridge.setTitle(("Ridge"))
        self.alphaLabel.setText(("Alpha"))
        self.alphaDoubleSpinBox.setToolTip(_translate("Form", "Regularization strength; must be a positive float. Regularization\n"
"improves the conditioning of the problem and reduces the variance of\n"
"the estimates. Larger values specify stronger regularization. Alpha\n"
"corresponds to C^-1 in other linear models such as LogisticRegression\n"
"or LinearSVC. If an array is passed, penalties are assumed to be specific\n"
"to the targets. Hence they must correspond in number.\n"
""))
        self.alphaDoubleSpinBox.setWhatsThis(("http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html"))
        self.copyXLabel.setText(("Copy X"))
        self.copyXCheckBox.setToolTip(("If True, X will be copied; else, it may be overwritten."))
        self.copyXCheckBox.setWhatsThis(("http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html"))
        self.fitInterceptLabel.setText(("Fit Intercept"))
        self.fitInterceptCheckBox.setToolTip(_translate("Form", "Whether to calculate the intercept for this model. If set to false,\n"
"no intercept will be used in calculations (e.g. data is expected to\n"
"be already centered)."))
        self.fitInterceptCheckBox.setWhatsThis(("http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html"))
        self.maxNumOfIterationsLabel.setText(("Max num of Iterations"))
        self.maxNumOfIterationslineEdit.setToolTip(_translate("Form", "Maximum number of iterations for conjugate gradient solver. For\n"
"\'sparse_cg\' and \'lsqr\' solvers, the default value is determined by\n"
"scipy.sparse.linalg. For \'sag\' solver, the default value is 1000.\n"
""))
        self.maxNumOfIterationslineEdit.setText(("None"))
        self.normalizeLabel.setText(("Normalize"))
        self.normalizeCheckBox.setToolTip(_translate("Form", "This parameter is ignored when fit_intercept is set to False. If True,\n"
"the regressors X will be normalized before regression by subtracting\n"
"the mean and dividing by the l2-norm. If you wish to standardize,\n"
"please use sklearn.preprocessing.StandardScaler before calling fit on\n"
"an estimator with normalize=False."))
        self.normalizeCheckBox.setWhatsThis(("http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html"))
        self.solverLabel.setText(("Solver"))
        self.toleranceLabel.setText(("Tolerance"))
        self.toleranceDoubleSpinBox.setToolTip(("Precision of the solution."))
        self.toleranceDoubleSpinBox.setWhatsThis(("http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html"))
        self.randomStateLabel.setText(("Random State"))
        self.randomStateLineEdit.setToolTip(_translate("Form", "The seed of the pseudo random number generator to use when shuffling\n"
"the data. If int, random_state is the seed used by the random number\n"
"generator; If RandomState instance, random_state is the random number\n"
"generator; If None, the random number generator is the RandomState\n"
"instance used by np.random. Used when solver == \'sag\'."))
        self.randomStateLineEdit.setWhatsThis(("http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html"))
        self.randomStateLineEdit.setText(("None"))
        self.solverComboBox.setToolTip(_translate("Form", "Solver to use in the computational routines:\n"
"\n"
"\'auto\' chooses the solver automatically based on the type of data.\n"
"\'svd\' uses a Singular Value Decomposition of X to compute the Ridge\n"
"coefficients. More stable for singular matrices than \'cholesky\'.\n"
"\'cholesky\' uses the standard scipy.linalg.solve function to obtain a\n"
"closed-form solution.\n"
"\'sparse_cg\' uses the conjugate gradient solver as found in\n"
"scipy.sparse.linalg.cg. As an iterative algorithm, this solver is more\n"
"appropriate than \'cholesky\' for large-scale data (possibility to set tol\n"
"and max_iter).\n"
"\'lsqr\' uses the dedicated regularized least-squares routine\n"
"scipy.sparse.linalg.lsqr. It is the fastest but may not be available in\n"
"old scipy versions. It also uses an iterative procedure.\n"
"\'sag\' uses a Stochastic Average Gradient descent, and \'saga\' uses its\n"
"improved, unbiased version named SAGA. Both methods also use an\n"
"iterative procedure, and are often faster than other solvers when both\n"
"n_samples and n_features are large. Note that \'sag\' and \'saga\' fast\n"
"convergence is only guaranteed on features with approximately the same\n"
"scale. You can preprocess the data with a scaler from\n"
"sklearn.preprocessing.\n"
"All last five solvers support both dense and sparse data. However, only\n"
"\'sag\' and \'saga\' supports sparse input when fit_intercept is True."))
        self.solverComboBox.setWhatsThis(("http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html"))
        self.solverComboBox.setItemText(0, ("auto"))
        self.solverComboBox.setItemText(1, ("svd"))
        self.solverComboBox.setItemText(2, ("cholesky"))
        self.solverComboBox.setItemText(3, ("lsqr"))
        self.solverComboBox.setItemText(4, ("sparse_cg"))
        self.solverComboBox.setItemText(5, ("sag"))
        self.crossValidateLabel.setText(("Cross Validate              "))
        self.crossValidateCheckBox.setToolTip(("Cross Validate"))
        self.crossValidateCheckBox.setWhatsThis(("http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

