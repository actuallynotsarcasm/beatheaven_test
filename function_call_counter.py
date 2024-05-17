class func_pbar:
    def __init__(self, target_iters, pbar=None):
        from functools import wraps
        from inspect import isawaitable
        self.wr = wraps
        self.is_async = isawaitable
        self.target_iters = target_iters
        self.first_call = True
        self.pbar_func = pbar

    def init_pbar(self):
        if not self.pbar_func:
            from tqdm import tqdm
            self.pbar = tqdm(total=self.target_iters, leave=False)
        else:
            self.pbar = self.pbar_func(total=self.target_iters, leave=False)
    
    def __call__(self, fn):
        @self.wr(fn)
        async def async_wrapper(*args, **kwargs):
            if self.first_call:
                self.first_call = False
                self.init_pbar()
            result = await fn(*args, **kwargs)
            self.pbar.update(1)
            return result
        
        @self.wr(fn)
        def wrapper(*args, **kwargs):
            if self.first_call:
                self.first_call = False
                self.init_pbar()
            result = fn(*args, **kwargs)
            self.pbar.update(1)
            return result
        
        if self.is_async(fn):
            return async_wrapper
        else:
            return wrapper