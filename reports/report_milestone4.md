# Milestone 4

## New Requirements

## 0 - New Requirements
|Package Name|Version|SHA-256|
|---|---|---|
|wandb|0.23.1|67431cd3168d79fdb803e503bd669c577872ffd5dadfa86de733b3274b93088e|

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
To run the docker image, the usage of the env-file must be explicitly stated by using the code: `docker run --env-file .env milestone4-modeltrainer` 

**Different Runs**
To test different hyperparameters, the image must be newly created and the container newly run every time.
