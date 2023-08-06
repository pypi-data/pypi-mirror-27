from SimpleFilter import *

sf = SimpleFilter()

'''

image_1 = sf.load('https://www.bluecross.org.uk/sites/default/files/assets/images/124044lpr.jpg',[200,200])
image_2 = sf.load('https://static.pexels.com/photos/126407/pexels-photo-126407.jpeg',[200,200])

conv_1 = sf.cycle(image_1,simple_filters,flat=True)
conv_2 = sf.cycle(image_2,simple_filters,flat=True)

result = sf.euc(conv_1,conv_2)

print(result)

'''

# Output >>> 10336.188050888552

image = sf.load('https://scontent-syd2-1.xx.fbcdn.net/v/t1.0-9/14573002_618095161712097_6362020796473104728_n.jpg?oh=d2500d35b1fc9d0e7dc38fd635d55ae1&oe=5A8A81AC',[200,200],convert='L')

sf.cycle(image,simple_filters5x5[0:2],3,plotall=True,col=None) # This will only use the first two filters in simple_filters

# Output below
