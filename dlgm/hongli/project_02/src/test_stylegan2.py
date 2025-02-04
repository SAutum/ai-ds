from torchinfo import summary
from stylegan2_pytorch.stylegan2_pytorch import StyleGAN2, Trainer


def test_trainer():
    trainer = Trainer(
        name='test',
        results_dir='results',
        models_dir='models',
        image_size=128,
        network_capacity=16,
        transparent=False,
        batch_size=4,
        mixed_prob=0.9,
        gradient_accumulate_every=4,
        lr=2e-4,
        lr_mlp=0.1,
        ttur_mult=1.5,
        num_workers=4,
        save_every=1000,
        evaluate_every=1000,
        generate=True,
        num_image_tiles=8,
        trunc_psi=0.75,
        fp16=True
    )


if __name__ == '__main__':
    # test the main model
    model = StyleGAN2(image_size=128)
    summary(model, (3, 128, 128), device='cpu')
