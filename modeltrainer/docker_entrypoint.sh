#!/bin/sh
set -e

wandb login "$WANDB_TOKEN"

exec "$@"
