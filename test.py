import torch


x = torch.linspace(-1,1, 2000)
y = torch.sin(x)

p = torch.tensor([1,2,3])

xx = x.unsqueeze(-1).pow(p)



model= torch.nn.Sequential(
    torch.nn.Linear(3, 4),
    torch.nn.Linear(4,1),
    torch.nn.Flatten(0,1)
)

learning_rate = 1e-3


loss_fn = torch.nn.MSELoss(reduction= 'sum')

optimizer = torch.optim.RMSprop(model.parameters(), lr = learning_rate)


for t in range(10000):

    y_pred = model(xx)


    loss = loss_fn(y_pred, y)

    if t%100 == 99:
        print(t+1, loss.item())
        
    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

linear_layer = model[0]

print(f'Result: y = {linear_layer.bias.item()} + {linear_layer.weight[:, 0].item()} x + {linear_layer.weight[:, 1].item()} x^2 + {linear_layer.weight[:, 2].item()} x^3')