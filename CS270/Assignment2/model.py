from __future__ import print_function
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F

class Custom_Network(nn.Module):
	def __init__(self):
		#super() function makes class inheritance more manageable and extensible
		super(Custom_Network, self).__init__()
		
		
		self.conv1 = nn.Conv2d(in_channels = 3, out_channels = 16, kernel_size = 5,
							  stride = 1, padding = 1 , padding_mode = 'zeros')
		self.conv2 = nn.Conv2d(in_channels = 16, out_channels = 32, kernel_size = 5,
							  stride = 1, padding = 1 , padding_mode = 'zeros')
		
		self.linear1 = nn.Linear(6272 , 256)
		self.linear2 = nn.Linear(256 , 84)
		self.linear3 = nn.Linear(84, 2)
		self.max1 = nn.MaxPool2d(kernel_size = 2, stride = 2)
		self.dropout = nn.Dropout(0.2)
		
	def forward(self, x):
		
		x = self.conv1(x)
		x = F.relu(x)
		x = self.max1(x)
		x = self.conv2(x)
		x = F.relu(x)
		x = self.max1(x)
		x = self.dropout(x)
		x = torch.flatten(x,1)
	
		x = x.view(-1, 6272)
		x = self.linear1(x)
		x = F.relu(x)
		x = self.linear2(x)
		x = F.relu(x)
		x = self.linear3(x)
		x = F.relu(x)
		output = F.log_softmax(x , dim = 1)
		return output
