#@title CRNN baseline

STAGE_ROOT = f"{OCR_RESEARCH_ROOT}/crnn/extended"

os.makedirs(STAGE_ROOT, exist_ok=True)

MAX_EPOCHS = 20
LEARNING_RATE = 1e-3
PATIENCE = 4
NUM_SAMPLE_PREDICTIONS = 3

CONFIG_PATH = f"{STAGE_ROOT}/config.json"
HISTORY_PATH = f"{STAGE_ROOT}/epoch_history.csv"
BEST_PATH = f"{STAGE_ROOT}/best_checkpoint.pt"
LAST_PATH = f"{STAGE_ROOT}/last_checkpoint.pt"
METRICS_PATH = f"{STAGE_ROOT}/metrics.json"
PREDICTIONS_PATH = f"{STAGE_ROOT}/predictions.csv"
SAMPLES_PATH = f"{STAGE_ROOT}/sample_predictions.txt"
README_PATH = f"{STAGE_ROOT}/README.md"


class CRNN(nn.Module):

    def __init__(self, num_classes):

        super().__init__()

        self.cnn = nn.Sequential(
            nn.Conv2d(1, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(128, 256, 3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),

            nn.Conv2d(256, 256, 3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(
                kernel_size=(2, 1),
                stride=(2, 1)
            ),

            nn.Conv2d(256, 512, 3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),

            nn.Conv2d(512, 512, 3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(
                kernel_size=(2, 1),
                stride=(2, 1)
            )
        )

        self.rnn = nn.LSTM(
            input_size=512,
            hidden_size=256,
            num_layers=2,
            bidirectional=True,
            dropout=0.2
        )

        self.classifier = nn.Linear(
            512,
            num_classes
        )

    def forward(self, x):

        x = self.cnn(x)

        x = F.adaptive_avg_pool2d(
            x,
            (1, x.size(3))
        )

        x = x.squeeze(2)

        x = x.permute(
            2,
            0,
            1
        )

        x, _ = self.rnn(x)

        x = self.classifier(x)

        return x


model = CRNN(
    num_classes=len(characters) + 1
).to(DEVICE)

criterion = nn.CTCLoss(
    blank=blank_idx,
    zero_infinity=True
)

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=LEARNING_RATE,
    weight_decay=1e-4
)

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="min",
    factor=0.5,
    patience=1
)


start_epoch = 1
best_cer = float("inf")
best_epoch = 0
epochs_without_improvement = 0
history = []


if os.path.exists(LAST_PATH):

    checkpoint = torch.load(
        LAST_PATH,
        map_location=DEVICE
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    optimizer.load_state_dict(
        checkpoint["optimizer_state_dict"]
    )

    if "scheduler_state_dict" in checkpoint:
        scheduler.load_state_dict(
            checkpoint["scheduler_state_dict"]
        )

    start_epoch = checkpoint["epoch"] + 1

    best_cer = checkpoint.get(
        "best_cer",
        float("inf")
    )

    best_epoch = checkpoint.get(
        "best_epoch",
        0
    )

    epochs_without_improvement = checkpoint.get(
        "epochs_without_improvement",
        0
    )

    if os.path.exists(HISTORY_PATH):

        history = pd.read_csv(
            HISTORY_PATH
        ).to_dict("records")

    print(f"Resuming | epoch {start_epoch}")

else:

    print("Starting CRNN")


config = {
    "model": "CRNN",
    "image_height": IMG_HEIGHT,
    "image_width": IMG_WIDTH,
    "vocabulary_size": len(characters),
    "num_classes": len(characters) + 1,
    "batch_size": BATCH_SIZE,
    "max_epochs": MAX_EPOCHS,
    "learning_rate": LEARNING_RATE,
    "patience": PATIENCE,
    "sample_predictions_per_epoch": NUM_SAMPLE_PREDICTIONS,
    "optimizer": "AdamW",
    "weight_decay": 1e-4,
    "loss": "CTCLoss",
    "seed": SEED,
    "train_samples": len(train_df),
    "validation_samples": len(val_df)
}


with open(
    CONFIG_PATH,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        config,
        f,
        indent=2,
        ensure_ascii=False
    )


def save_checkpoint(
    path,
    epoch,
    best_cer,
    best_epoch,
    epochs_without_improvement
):

    torch.save(
        {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "scheduler_state_dict": scheduler.state_dict(),
            "best_cer": best_cer,
            "best_epoch": best_epoch,
            "epochs_without_improvement": epochs_without_improvement,
            "char_to_idx": char_to_idx,
            "idx_to_char": idx_to_char,
            "blank_idx": blank_idx,
            "config": config
        },
        path
    )


def save_stage_readme():

    with open(
        README_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "# CRNN Extended Training\n\n"
            "Initial CRNN OCR training stage for handwritten "
            "Amharic text recognition.\n\n"
            "## Configuration\n\n"
            f"- Training samples: {len(train_df)}\n"
            f"- Validation samples: {len(val_df)}\n"
            f"- Image size: {IMG_WIDTH}x{IMG_HEIGHT}\n"
            f"- Batch size: {BATCH_SIZE}\n"
            f"- Maximum epochs: {MAX_EPOCHS}\n"
            f"- Optimizer: AdamW\n"
            f"- Learning rate: {LEARNING_RATE}\n"
            f"- Validation split: writer-disjoint\n"
            f"- Sample predictions per epoch: {NUM_SAMPLE_PREDICTIONS}\n"
        )


save_stage_readme()


for epoch in range(
    start_epoch,
    MAX_EPOCHS + 1
):

    model.train()

    running_loss = 0.0
    batch_count = 0

    for images, targets, target_lengths in train_loader:

        images = images.to(
            DEVICE,
            non_blocking=True
        )

        targets = targets.to(
            DEVICE
        )

        optimizer.zero_grad(
            set_to_none=True
        )

        outputs = model(images)

        input_lengths = torch.full(
            size=(images.size(0),),
            fill_value=outputs.size(0),
            dtype=torch.long,
            device=DEVICE
        )

        loss = criterion(
            outputs.log_softmax(2),
            targets,
            input_lengths,
            target_lengths.to(DEVICE)
        )

        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            model.parameters(),
            max_norm=5.0
        )

        optimizer.step()

        running_loss += loss.item()
        batch_count += 1

    train_loss = running_loss / batch_count

    evaluation = evaluate_model(
        model,
        val_loader
    )

    val_cer = evaluation["cer"]
    val_wer = evaluation["wer"]
    exact_accuracy = evaluation["exact_accuracy"]

    scheduler.step(val_cer)

    improved = val_cer < best_cer

    if improved:

        best_cer = val_cer
        best_epoch = epoch
        epochs_without_improvement = 0

        save_checkpoint(
            BEST_PATH,
            epoch,
            best_cer,
            best_epoch,
            epochs_without_improvement
        )

        save_predictions(
            evaluation["references"],
            evaluation["predictions"],
            PREDICTIONS_PATH
        )

        sample_lines = []

        for reference, prediction in zip(
            evaluation["references"][:20],
            evaluation["predictions"][:20]
        ):

            sample_lines.append(
                f"GT: {reference}\n"
                f"PR: {prediction}\n"
            )

        with open(
            SAMPLES_PATH,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "\n".join(sample_lines)
            )

    else:

        epochs_without_improvement += 1

    epoch_record = {
        "epoch": epoch,
        "train_loss": train_loss,
        "val_cer": val_cer,
        "val_wer": val_wer,
        "exact_accuracy": exact_accuracy,
        "learning_rate": optimizer.param_groups[0]["lr"],
        "best_cer": best_cer,
        "best_epoch": best_epoch
    }

    history.append(epoch_record)

    pd.DataFrame(
        history
    ).to_csv(
        HISTORY_PATH,
        index=False
    )

    save_checkpoint(
        LAST_PATH,
        epoch,
        best_cer,
        best_epoch,
        epochs_without_improvement
    )

    save_metrics(
        {
            "current_epoch": epoch,
            "best_epoch": best_epoch,
            "best_cer": best_cer,
            "current_cer": val_cer,
            "current_wer": val_wer,
            "current_exact_accuracy": exact_accuracy
        },
        METRICS_PATH
    )

    print(
        f"\nEpoch {epoch:02d} | "
        f"loss {train_loss:.4f} | "
        f"CER {val_cer:.4f} | "
        f"WER {val_wer:.4f}"
        + (" | best" if improved else "")
    )

    for reference, prediction in zip(
        evaluation["references"][:NUM_SAMPLE_PREDICTIONS],
        evaluation["predictions"][:NUM_SAMPLE_PREDICTIONS]
    ):

        print(f"GT: {reference}")
        print(f"PR: {prediction}")

    if epochs_without_improvement >= PATIENCE:

        print(
            f"Early stop | best epoch {best_epoch}"
        )

        break


print(
    f"\nDone | best epoch {best_epoch} | "
    f"CER {best_cer:.4f}"
)