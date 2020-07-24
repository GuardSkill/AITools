import torch


def pytorch_fix_seed(seed):
    use_cuda = torch.cuda.is_available()
    torch.manual_seed(seed)
    if use_cuda:
        torch.cuda.manual_seed(seed)
    np.random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
