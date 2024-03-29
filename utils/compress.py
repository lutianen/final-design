import copy, torch, math, random
import numpy as np
from scipy.spatial import distance

# TODO reconstruction functions with class

def sparsify(model, compress_cr, v, dist_type: str="abs"):
    if dist_type == "base_line":
        return _base_line()

    for name, param in model.named_parameters():
        if param.grad is None: # 由于只使用了 G，因此需要派出 D 相关的梯度
            continue

        grad = param.grad.data
        if torch.is_tensor(grad):
            num_reserved = int(math.ceil(grad.numel() * compress_cr))
            if dist_type != "random":
                grad_norm = _importance(grad, num_reserved, dist_type)
                threshold = torch.min(torch.topk(grad_norm, num_reserved, 0, largest=True, sorted=False)[0])
                mask = torch.ge(grad_norm, threshold)
                indices = torch.nonzero(mask).view(-1)[:num_reserved] # tensor([ 42,  44,  53, 141, 143], device='cuda:0')
            else:
                indices = torch.tensor(random.sample(range(0, grad.numel() - 1), num_reserved)).to(grad.device)
            param.grad.data = _update(grad, indices, name, v)
        else:
            raise Exception("grad must be tensor!")

def _importance(grad: torch.Tensor, num_reserved: int, dist_type: str="abs"):
    if dist_type == "gcc":
        return _gcc(grad)
    elif dist_type == "l1":
        return _l1(grad)
    elif dist_type == "abs":
        return _abs(grad)
    else:
        raise Exception("dist_type must be in [l2, cos, l1, abs]")

def _update(grad, indices, name, v):
    '''Update grad with gradient accumulate.
        return: the gradient of updated.
    '''

    v_vec = v[name].view(-1)
    v_vec += grad.view(-1)
    A = torch.zeros_like(v_vec).to(grad.device)

    A = copy.deepcopy(v_vec)
    A.index_fill_(0, indices, 0)
    A = -A
    A += v_vec
    v_vec.index_fill_(0, indices, 0)

    v[name] = v_vec.view(v[name].shape)
    return A.view(v[name].shape)

def _base_line():
    return

def _gcc(grad: torch.Tensor):
    grad_vec = grad.view(grad.numel(), -1)
    grad_norm = torch.norm(grad_vec, 2, 1, keepdim=True)
    grad_mean = torch.mean(grad_norm)
    return torch.cdist(grad_vec, grad_mean.view(1, 1)).view(-1)
    
    """
    _numel = grad.numel()
    grad_vec = grad.view(_numel, -1)
    similar = torch.zeros(_numel).cuda()
    for idx, item in enumerate(grad_vec):
        similar[idx] = torch.sum(torch.abs(torch.cdist(item.view(1, 1), grad_vec)))
    return similar
    """

    """
    grad_vec = grad.view(grad.numel(), -1)
    # FIXME
    grad_norm = torch.norm(grad_vec, 2, 1, keepdim=True) # type: ignore

    # On CPU
    # grad_norm_np = grad_norm.cpu().numpy()
    # similar_matrix = distance.cdist(grad_norm_np, grad_norm_np, 'euclidean')
    # similar_sum = np.sum(np.abs(similar_matrix), axis=0)
    # return torch.from_numpy(similar_sum).to(grad.device)

    # On GPU
    similar_matrix = torch.cdist(grad_norm, grad_norm)
    # FIXME
    similar_sum = torch.sum(torch.abs(similar_matrix), axis=0) # type: ignore
    return similar_sum
    """

def _l1(grad: torch.Tensor):
    grad_vec = grad.view(grad.numel(), -1)
    grad_norm = torch.norm(grad_vec, 1, 1, keepdim=True)
    grad_mean = torch.mean(grad_norm)
    return torch.cdist(grad_vec, grad_mean.view(1, 1)).view(-1)

    """
    _numel = grad.numel()
    grad_vec = grad.view(_numel, -1)
    similar = torch.zeros(_numel).cuda()
    for idx, item in enumerate(grad_vec):
        similar[idx] = torch.sum(torch.abs(torch.cdist(item.view(1, 1), grad_vec)))
    return similar
    """

    """
    grad_vec = grad.view(-1, 1)
    # FIXME
    grad_norm = torch.norm(grad_vec, 1, 1, keepdim=True) # type: ignore

    # # On CPU
    # grad_norm_np = grad_norm.cpu().numpy()
    # similar_matrix = 1 - distance.cdist(grad_norm_np, grad_norm_np, 'cosine')
    # similar_sum = np.sum(np.abs(similar_matrix), axis=0)
    # return torch.from_numpy(similar_sum).to(grad.device)

    # On GPU
    similar_matrix = torch.cdist(grad_norm, grad_norm)
    # FIXME
    similar_sum = torch.sum(torch.abs(similar_matrix), axis=0) # type: ignore
    return similar_sum
    """

def _abs(grad: torch.Tensor):
    """
        grad: [input, output, kernel, kernel]
        return: [input * output * kernel * kernel] 
    """
    grad_vec = grad.view(-1)
    return torch.abs(grad_vec)
