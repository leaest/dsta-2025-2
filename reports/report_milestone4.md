# Milestone 4

## New Requirements

## 0 - New Requirements
|Package Name|Version|SHA-256|
|---|---|---|
|wandb|0.23.1|67431cd3168d79fdb803e503bd669c577872ffd5dadfa86de733b3274b93088e|
|jupyter|1.1.1|7a59533c22af65439b24bbe60373a4e95af8f16ac65a6c00820ad378e3f7cc83|
|matplotlib|3.10.8|ee40c27c795bda6a5292e9cff9890189d32f7e3a0bf04e0e3c9430c4a00c37df|
|pandas|2.3.3|dd7478f1463441ae4ca7308a70e90b33470fa593429f9d4c578dd00d1fa78838|

## 1 - Theory
**Experiment Management**
In the context of machine learning, the term experiment management refers to the process of tracking and organizing experiment metadata, which can then be accessed and shared within a team. This metadata typically includes code and data versions, hyperparameters, environment configurations, and performance metrics.

Experiment management allows us to share and reproduce results. It also ensures that long-running experiments are saved and documented. Overall, it is important because we want to track changes and understand why a model performs better or worse than another.

**Metrics**
Metrics are used to monitor and measure the performance of a model. They vary depending on the type of model, e.g., classification or regression. Choosing the correct metric for each task is crucial, otherwise, the results may not accurately reflect the model’s true performance.

**Confusion Matrix**
The confusion matrix summarizes classification performance by comparing predicted and actual class labels. It highlights where a model is making mistakes and provides a basis for calculating key metrics such as precision and recall.

|  |Predicted Positive|Predicted Negative|
|---|---|---|
|**Actual Positive**|True Positive (TP)|False Negative (FN)|
|**Actual Negative**|False Positive (FP)|True Negative (TN)|

**Precision and Recall**
Using the confusion matrix, we can calculate precision and recall:

*Precision* describes the proportion of predicted positive instances that are actually positive. It is defined as:
$$
\text{Precision} = \frac{\text{correctly classified actual positives}}{\text{everything classified as positives}} = \frac{\text{TP}}{\text{TP + FP}}
$$

This concept can be easily illustrated using the spam-mail analogy:
$$
\text{Precision} = \frac{\text{number of emails correctly predicted as spam}}{\text{total number of emails predicted as spam}}
$$

Precision measures how many of the predicted positive instances are correct, minimizing false positives.
___
*Recall* (or true positive rate) describes the proportion of actual positive instances that are correctly identified. It is defined as:
$$
\text{Recall} = \frac{\text{correctly classified actual positives}}{\text{all actual positives}} = \frac{\text{TP}}{\text{TP + FN}}
$$

Using the spam-mail analogy:
$$
\text{Recall} = \frac{\text{number of emails correctly predicted as spam}}{\text{total number of actual spam emails}}
$$

Recall measures how many of the actual positive instances are identified correctly, minimizing false negatives.
___

Although precision and recall may seem similar, there is a **critical trade-off** between them. Raising the classification threshold usually decreases false positives but increases false negatives. As a result, precision and recall often have an inverse relationship. Depending on the costs, benefits, and risks associated with false positives and false negatives, one metric may be prioritized over the other.

**AUROC**
AUROC (Area Under the Receiver Operating Characteristic Curve) is a widely used metric for binary classification tasks. The ROC curve plots the false positive rate (FPR) on the x-axis and the true positive rate (TPR) on the y-axis for different classification thresholds. AUROC measures the area under this curve.

Interpretation:
- 0.5: The model performs no better than random guessing
- 1.0: The model perfectly separates positive and negative classes

AUROC evaluates how well a model can distinguish positive from negative samples across all possible thresholds, providing a threshold-independent measure of performance.

## Task 2
We reused the Docker container that we created in milestone 2 and extended it with experiment tracking via Weights & Biases. Therefor, all the changes to the code only concern files in the folder "modeltrainer".

**Pyhton Code Changes**
In the `main.py` a new codeblock was added, in which the hyperparameters for the model training process are defined. This configuration includs all relevant paramenters, such as:
    - Optimizer
    Loss function
    Batch size
    Number of epochs
    Network architecture parameters

Training and validation metrics are logged using the official W&B Keras integration. Since the newer packages use a different import call: `wandb.integration.keras` as noted in their updated documentation[https://docs.wandb.ai/models/integrations/keras?utm_source=chatgpt.com]

Furthermore, it was necessary to adjust the `neuralnet_training.py`. On the one hand a argument to log the metrics (`callbacks=[WandbMetricsLogger()]`) was added in the `model.fit()`-function. On the other hand the code was changed so that now all hyperparameters are  defined in the Weights & Biases configuration in the `main.py` and are passed directly to the training. This ensures consistency and makes it easier to play around with the hyperparameters.

Lastly, a code snipped was added that saves the predictions from the model of a run to a csv-file and automatically uploads it to W&B.

**Login settings**
To ensure that the login credentials remain secret but still work with the `Dockerfile` several steps were necessary.

After creating a account on the W&B Website[https://wandb.ai/login] and you are in the quickstart menu to create a new model, you are shown a token that can be used to log into your account. Since this key must remain secret, a special approach is required.

First a new file where that key can be stored must be created. However, since this key must remain secret it should NOT be pushed / tracked by github. Therefor it makes sense to use `.env` file. In this file the API key can safely be stored using the following code:

```env
WANDB_TOKEN=YOUR_API_KEY
```
Second, a entrypoint file is created. This file ensures that the login into W&B occurs before the training begins. This file is called `docker_entrypoint.sh`. It first reads the WANDB_TOKEN from the `.env` file. The `exec "$@"` tells the container that now the program, in this case the `main.py` can be run. The entrypoint script must be made executable with the command `chmod +x docker_entrypoint.sh`.

To ensure that others working on the same code can commit to the same W&B projects, the attributes in the `main.py` regarding the project (`milestone4_modeltrainer`) ,and the entity (`DSTA-2025`) must remain the same. Furthermore the collaborators must belong to the that specified team (`DSTA-2025`). Then they themselves must create a `.env` file with their personal API key.

Inside the Dockerfile the `RUN chmod +x /app/docker_entrypoint.sh` gives permission to let the script be run as a program inside the docker image. The `ENTRYPOINT ["/app/docker_entrypoint.sh"]` tells Docker to run the entypoint script before the `main.py`.

To build the image the following code was used: `docker build -t milestone4-modeltrainer .`.
To run the docker image, the usage of the env-file must be explicitly stated by using the code: `docker run --env-file .env milestone4-modeltrainer`.

**Different Runs**
To test different hyperparameters, the image must be newly created and the container newly run every time.

The results of the training run can be inspected under the the project (DSTA-2025)[https://wandb.ai/dsta-2025/milestone4_modeltrainer]

## Task 3
The Jupyter notebook is stored in the folder "notebooks". To use Jupyter Notes the package jupyter had to be installed. Since we are not allowed to use sudo, the virtual environment created a the very beginning had to be started with the regular command: `source .venv/bin/activate`. Then, all the required packages (matplotlib) could be installed. I created a `requirements-jupyter.txt` file with the `pip freeze` command inside the notebooks folder, since these libraries are not required for the docker images, they are however, to successfully look at the jupyter notebook.
After having started the virtual environment and installed all packages the jupyter server can be started with the command `jupyter notebook`. The server should start up and provide a link that will open the local server in the browser. It is usually something similar to: `http://localhost:8888/...`.
Then a new notebook can be created or one that already exists can be opened up. Inside the notebook there are two types of cells, code-cells that contain runable code and markdown-cells that can be styled with markdown syntax.

In the notebook Milestone4.ipynb the first block imported the python libraries that were required. In the second code cell the MINST data was loaded, using the keras function.
Code cell three and four contain python code that create plots. The first plot shows the distribution of digits across the entire training dataset. The second plot shows how an average figure of each digit would look like.

In the second chapter in the Jupyter Notebook the predictions and the ground-of-truth data is downloaded from a specific W&B run (sweet-shape21)[https://wandb.ai/dsta-2025/milestone4_modeltrainer/runs/803djk5d]. I chose this model simply because it was the first that offered a clean downloadable prediction dataset. The model was then analyzed with a confusion matrix.
In order for anyone else to use the Jupyter Notebook, they must have an account at W&B and then follow the prompts inside the notebook, in order to download the prediction data and run the analysis.


**Version Control Jupyter Notebooks**
It is difficult to use version control on Jupyter Notes with Github because Git is only intended for human-readable code. The problem with Jupyter Notebooks is, that it not only stores the code but also its output in Json-Format. As a result, even small changes can produce large and difficult-to-read differences when tracked with Git.
This makes it hard to review changes, resolve merge conflicts, or understand what was actually modified between versions.