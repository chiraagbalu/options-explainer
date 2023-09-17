import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Define the Streamlit app
st.title("Options Explainer")


st.write("""## Key Idea of Options

Options let us express beliefs on how wiggly the price of a stock is (also known as its 'volatility')

### What's an Option?

Options are kind of like coupons. 

Let’s say Nike is selling coupons for a pair of basketball shoes, at **10 dollars per coupon**. 

Each coupon will let you buy **2 pairs of LeBron shoes** for **200 dollars each**. 

The coupons **expire in 1 month**, so you have some time to decide to use the coupon. 

These coupons have:
- **a price** (you have to pay money for the coupon)
- **a way to transact** (you get to buy something for a specified price)
- **an underlying asset** (you get to buy a pair of LeBrons)
- **an expiry date** (you get to buy a pair of LeBrons until 1 month from now)
- **a price to transact at** (you get to buy a pair LeBrons at 200 dollars until 1 month from now)
- **a quantity** (you get to buy 2 pairs of LeBrons at 200 dollars each until 1 month from now)

You decide to buy some coupons

How do we know how much these coupons are worth? 

If a pair of Lebrons cost 190 dollars each right now, do you really want to use the coupon? Probably not, since you can just buy the shoes from Nike instead. So the coupon likely isn’t worth much. 

But let’s say LeBron wins the finals with the Lakers next week (hypothetically). Suddenly, the LeBrons are flying off the shelves, and Nike jacks up the prices to 300 dollars a pair!

How are we feeling? Pretty good I’d imagine! We can buy each pair of LeBrons for 100 dollars off the retail price.

Since we expect there's a lot of people willing to buy the shoe, we might even buy the 2 pairs of shoes for 200 dollars each, and sell them to someone else for 300 dollars each. 
This means we'd make 190 dollars! 

Can you see why? 

""")

st.latex('''(300-200) \\times 2 - 10 = 100 \\times 2 - 10 = 200 - 10 = 190''')

st.write("""
Generalizing this formula:
""")

st.latex('''(\\text{Nike Price} - \\text{Discounted Price}) \\times (n \\text{ pairs of shoes per coupon}) - (\\text{coupon price})''')


st.write("""
So if we know the coupon is expiring today, we can pretty easily plot out the profit we might get from the using the coupon, as a function of Nike's retail price.

Notice that when the shoes are worth anything less than 200 dollars, we simply don't use our coupon - since we'd just be losing money. 
""")


min_price_initial = 50
max_price_initial = 400

strike_price_initial = 200
premium_initial = 10

underlying_prices_plot = np.linspace(min_price_initial, max_price_initial, 8)

def calculate_long_call_payoff(underlying_prices, strike_price, premium):
    payoffs = np.where(underlying_prices <= strike_price, -premium, (underlying_prices - strike_price) - premium)
    return payoffs

payoffs_plot = calculate_long_call_payoff(underlying_prices_plot, strike_price_initial, premium_initial)

fig = px.line(x=underlying_prices_plot, y=payoffs_plot, labels={"x": "LeBron Shoe Value", "y": "Profit"})
fig.update_layout(
    title=f"Coupon Profit Diagram",
    xaxis_title="LeBron Shoe Value",
    yaxis_title="Profit"
)

st.plotly_chart(fig)


st.write("""
This is pretty cool! Looks like we have a ton of upside (potentially infinite), and not very much downside (what we paid for the coupon, 10 dollars). 

Play around with the parameters a bit, try to answer the following questions/do the following:

TODO: make simulations load faster, whole page reloads whenever you change a parameter so i would like to isolate that somehow

TODO: make these exploration questions better lol

- what happens when the coupon price is above the maximum of the price range?
- what happens when the coupon price is below the minimum of the price range?
- what's the relation between the price paid for the coupon, coupon price, and the min/max price range?
""")

strike_price_input = st.slider(
    'Select the discounted price to buy shoes at!',
    0, 1000, 200)

premium_input = st.slider(
    'Select the price we paid for the coupon!',
    0, 1000, 10)

underlying_prices_shoes = np.linspace(0, 1000, (1000))

payoffs_shoes = calculate_long_call_payoff(underlying_prices_shoes, strike_price_input, premium_input)

fig2 = px.line(x=underlying_prices_shoes, y=payoffs_shoes, labels={"x": "LeBron Shoe Value", "y": "Profit"})
fig2.update_layout(
    title=f"Coupon Profit Diagram",
    xaxis_title="LeBron Shoe Value",
    yaxis_title="Profit"
)

st.plotly_chart(fig2)

st.write("""

### Another Kind of Option

Now that we've done some exploration, let's talk about another variant of an option. 

Imagine instead of being able to buy an object for a specified price before some specified expiration date, we can sell an object instead. 

For example, imagine you have a designer handbag that a coworker of yours has always wanted. 

She's saving up for her own bag, but she's willing to buy your bag off of you anytime within the next year, for 1500 dollars. 
She'll guarantee to do this trade with you, if you pay her 100 dollars up front. 

Like before, this deal has:
- **a price** (you have to pay money to guarantee the deal)
- **a way to transact** (you get to sell something for a specified price)
- **an underlying asset** (you get to sell your handbag)
- **an expiry date** (you get to sell handbags until 1 year from now)
- **a price to transact at** (you get to sell handbags at 1500 dollars until 1 year from now)
- **a quantity** (you get to buy 1 handbag at 1500 dollars each until 1 year from now)

The handbag is worth 2000 dollars right now, so you have no reason to sell it to her for 1500 dollars. 
But like before with the LeBron shoes - something might happen that could cause your handbag's value to drop dramatically. 

Let's say you agree to her deal. 

A few months later, handbags are falling out of fashion. In a shocking twist, backpacks have become all the rage, and the one-sided handbags are seen as trashy. 
Your handbag is only worth 200 dollars now! (it is still very high quality)

You call your coworker and give her the handbag. She's a bit upset, but upholds her end of the bargain. 

How much money did you just make, in theory? 
You sold something that was worth 200 dollars for 1500 dollars, and you only paid 100 dollars to be able to do that, so you've made 1200 dollars!
""")

st.latex('''(1500-200) \\times 1 - 100 = 1300 \\times 1 - 100 = 1300 - 100 = 1200''')

st.write("""
Generalizing this formula:
""")

st.latex('''(\\text{Coworker Price} - \\text{Handbag Price}) \\times (n \\text{ handbags per deal}) - (\\text{deal price})''')

st.write(""" Just like before, we can plot the theoretical profit we'd have had one year out, depending on how much our handbag ended up being worth.

Notice again that when the handbag is worth anything more than 1500 dollars, we simply don't sell it to our coworker - since we'd just be losing money. 

""")

min_price_bag = 100
max_price_bag = 2000

strike_price_bag = 1500
premium_bag = 200

underlying_prices_bag = np.linspace(min_price_bag, max_price_bag, max_price_bag-min_price_bag)

def calculate_long_put_payoff(underlying_prices, strike_price, premium):
    put_payoffs = np.where(underlying_prices <= strike_price, (strike_price - underlying_prices) - premium, -premium)
    return put_payoffs

payoffs_bag = calculate_long_put_payoff(underlying_prices_bag, strike_price_bag, premium_bag)

fig_bag = px.line(x=underlying_prices_bag, y=payoffs_bag, labels={"x": "Designer Handbag Value", "y": "Profit"})
fig_bag.update_layout(
    title=f"Coworker Deal Profit Diagram",
    xaxis_title="Designer Handbag Value",
    yaxis_title="Profit"
)

st.plotly_chart(fig_bag)

st.write("""

### What does this have to do with options?

What we've just described here **are** options!

Options come in two types, **Calls** and **Puts**.

Like with the Nike Coupons, Call Options allow you to buy a fixed amount of some asset (for example, stocks), at a specified price until an expiration date.

And like with the Coworker Handbag Deal, Put Options allow you to sell a fixed amount of some asset (for example, stocks), at a specified price until an expiration date.

They're called 'options' because you don't have to exercise them! 

If the LeBrons had never increased in price, we wouldn't want or need to use them, so all we'd lose is the amount we paid for the coupon.

Same situation for the handbag, we didn't exercise the option to sell it to our coworker because it wouldn't be profitable for us.

Before we move on, let's quickly go over some terminology, so that everyone is on the same page. 

### Terminology

- The specified price that we transact at in an option is its **STRIKE PRICE**

- The price that we pay for an option is its **PREMIUM**

- The amount of the asset that we trade in an option is its **MULTIPLIER** (stock options are usually 100)

- The expiration date is the ... **EXPIRATION DATE** (no fancy name here)

We can describe an option by using the following structure

{Asset} {Expiration Date or Days to Expiry} {Strike Price} {Call/Put} @ {Premium}

Think about what the options we talked about earlier might be described as

LeBron 30DTE 200c @ 10 dollars

Handbag 365DTE 1500p @ 100 dollars

### How much should options cost?

What does any of this have to do with the key idea of volatility? 

It mostly comes from how we price these options.

Let's use a very simple underlying asset to start with: a die.

I'm going to roll the die, and the value of the die will be the amount of dots on the face-up side of the die. 

So if the die comes up 6, the asset is worth 6 dollars. 

You can assume the die is fair, so there's an equal chance that each face comes up on top.

How much should the 4 dollar strike be worth (or what is its premium)? Let's say that the multiplier is 1 (just one die) and that the expiration is after the dice is rolled, and its price is determined. 

We'll start by randomly guessing and vibing out some basic ideas. 

Pretend it's worth 1 cent. Seems a bit cheap, right? We could buy it for a cent a bunch of times, and expect to make more than a cent most of the time - so that's probably too cheap. (Why?)

What if it's worth 2 dollars?
That seems a bit high, we could sell it to someone at that price a bunch of times and expect to make money almost every time, since it's never going to pay out more than 2 dollars. (Why?) 

So the answer is somewhere in between these bounds. 

We can try to figure out how much the option is worth by simulating the dice roll a bunch of times, and finding the average value of the option over time.

Let's roll a dice 100,000 times, and plot a histogram of the rolls that we get


""")



def roll_dice():
    return np.random.randint(1, 7)


dice_strike = st.slider("Select the strike price of the option", 1, 6, 3)

# Generate random dice rolls
rolls = [roll_dice() for _ in range(100000)]

hist, bin_edges = np.histogram(rolls, bins=6, range=(1, 7))

# Define colors based on bin values
colors = ['green' if bin_value > dice_strike else 'red' for bin_value in bin_edges[0:]]

# Create a bar chart using Plotly
fig_dice = go.Figure()
fig_dice.add_trace(go.Bar(
    x=bin_edges[0:],
    y=hist,
    marker_color=colors,
    text=hist,
    textposition='outside'
))

# Update the layout
fig_dice.update_layout(
    title=f"Dice Roll Histogram (Strike Price: {dice_strike})",
    xaxis_title="Dice Value",
    yaxis_title="Frequency"
)

# Display the histogram
st.plotly_chart(fig_dice)

st.write("""We'll also plot out the payoff, or profit, of having that option for each roll:

Red means the option ended up being worth 0 after the die roll, and green means it was worth a positive amount, denoted by the value at the bottom of the bar
""")

dice_payoffs = [roll-dice_strike if roll > dice_strike else 0 for roll in rolls]

hist_payoffs, bin_edges_payoffs = np.histogram(dice_payoffs, bins=7-dice_strike, range=(0, 7-dice_strike))

# Define colors based on bin values
colors_dice_payoffs = ['green' if bin_value > 0 else 'red' for bin_value in bin_edges_payoffs[0:]]

# Create a bar chart using Plotly
fig_dice_payoff = go.Figure()
fig_dice_payoff.add_trace(go.Bar(
    x=bin_edges_payoffs[0:],
    y=hist_payoffs,
    marker_color=colors_dice_payoffs,
    text=hist_payoffs,
    textposition='outside'
))

# Update the layout
fig_dice_payoff.update_layout(
    title=f"Dice Call Option Payoff Histogram (Strike Price: {dice_strike})",
    xaxis_title="Option Payoff",
    yaxis_title="Frequency"
)

st.plotly_chart(fig_dice_payoff)

probabilities = hist_payoffs / np.sum(hist_payoffs)
expected_value = np.sum(probabilities * bin_edges_payoffs[:-1])

latex_string_dice = ""

for i in range(len(probabilities)):
    if i == len(probabilities)-1:
        latex_string_dice += f"{probabilities[i]} \\times {bin_edges_payoffs[i]} = {expected_value}"
    else:
        latex_string_dice += f"{probabilities[i]} \\times {bin_edges_payoffs[i]} + "
        
st.write("""
Now we can calculate the average price of the option over the 100,000 rolls, and that should be pretty close to what the option is actually worth!

We multiply each payoff by the probability of getting each of the payoffs, and add them all together, effectively a weighted average

So for each outcome $i$
""")

st.latex('''
\\text{average value} = \\sum_i^n \\text{probability of outcome i} \\times \\text{payoff of outcome i}''')

st.write(""" plugging in the values from the histogram above, we find that the strike selected's average value is: """)

st.latex(latex_string_dice)

st.write("""
This is pretty much how options are priced in the real world, on just about any asset!

1. Come up with a distribution of the possible prices of the asset on the day of the expiry.
2. Estimate or simulate the probability that each price happens
3. Figure out how much the option is worth for each price
4. Find the average value of the option based on the probability distribution of prices

Here, we 
1. Came up with the distribution of possible prices (1-6 are the possible faces of a die)
2. Estimated the probability of each possible price by simulating (roughly 1/6 since it's a fair die)
3. Figured out how much the option is worth for each price (Die Value - Strike Price whenever the Die Value > Strike Price)
4. Found the average value of the option based on the probability distribution of prices (multiplied each outcome by its probability, weighted average)

### What does this have to do with stocks?

It's the exact same process!

1. Come up with a distribution of the possible prices of the asset on the day of the expiry.
2. Estimate or simulate the probability that each price happens

Here's how we're going to simulate a stock's potential future paths:

- start with the current price of the stock
- for each time step:
  - we choose an amount for the stock to move (the stock's return at the current timestep)
  - we choose the amount for the stock to move from a symmetrical bell curve of possible amounts (sampling fro a normal distribution)
  - the width of the bell curve is the stock's 'volatility' (this is the standard deviation of the return distribution)
  - a higher volatility means a wider bell curve, so the movements will usually be further from the average (higher volatility -> the stock path will jump around more)
  - a lower volatility means a tighter bell curve, so the movements will usually be closer to the average (lower volatility -> the stock path will be more smooth)
  - simulate the stock moving that amount
  - set the new current price to be the price after the stock moved
  


There's some technical detail being glossed over in the above explanation, but feel free to look up geometric brownian motion if you want to learn more about the specifics!
""")

def simulate_gbm_paths(s0, mu, sigma, n=24, T=30, num_paths=1000, plot=True):
    dt = 1/n
    t = np.linspace(0, T, n*T+1)
    S = np.zeros((num_paths, n*T+1))
    
    for i in range(num_paths):
        W = np.random.standard_normal(size=n*T+1)
        W = np.cumsum(W)*np.sqrt(dt)
        X = (mu-0.5*sigma**2)*t + sigma*W
        S[i,:] = s0*np.exp(X)
        
        
    fig_paths = go.Figure()
    for i in range(num_paths):
        fig_paths.add_trace(go.Scatter(x=t, y=S[i,:], mode='lines', name=f'Path {i+1}'))

    fig_paths.update_layout(
        title='Simulated Stock Paths',
        xaxis_title='Time',
        yaxis_title='Price',
        showlegend=True,
        width=800,
        height=500,
    )
    if plot:
        st.plotly_chart(fig_paths)


simulate_gbm_paths(s0=200, mu=0.0005, sigma=0.005, n=24, T=30, num_paths=10, plot=True)

st.write("""Now that we've simulated some paths, let's look at the distribution of outcomes these paths might create! 

Let's generate a lot more paths: 100 should be a good number to start with
""")



def simulate_gbm_paths_plotly_histogram_with_bins(s0, mu, sigma, n=24, T=30, num_paths=1000, num_bins=20):
    dt = 1/n
    t = np.linspace(0, T, n*T+1)
    S = np.zeros((num_paths, n*T+1))
    
    for i in range(num_paths):
        W = np.random.standard_normal(size=n*T+1)
        W = np.cumsum(W)*np.sqrt(dt)
        X = (mu-0.5*sigma**2)*t + sigma*W
        S[i,:] = s0*np.exp(X)
    
    # Calculate end values
    end_values = S[:, -1]
    
    # Calculate histogram data
    hist_values, bin_edges = np.histogram(end_values, bins=num_bins)
    
    # Create subplots with one row and two columns
    fig = make_subplots(rows=1, cols=2, subplot_titles=('GBM Paths', 'End Value Histogram'), column_widths=[0.7, 0.3])
    
    # Add GBM paths to the first subplot
    for i in range(num_paths):
        fig.add_trace(go.Scatter(x=t, y=S[i,:], mode='lines', name=f'Path {i+1}'), row=1, col=1)

    
    # Add a bar chart with bins and counts to the second subplot
    fig.add_trace(go.Bar(y=bin_edges[:-1], x=hist_values, orientation='h', name='End Values'), row=1, col=2)
    
    # Update layout
    fig.update_layout(
        title='Simulated Stock Paths and Expiration Price Distribution',
        xaxis_title='Counts',
        yaxis_title='Price',
        xaxis2=dict(domain=[0.75, 1.0]),
        yaxis2=dict(anchor='x2'),
        showlegend=False,  # Set to False to avoid legend duplication
        width=1000,
        height=500,
    )
    
    st.plotly_chart(fig)

simulate_gbm_paths_plotly_histogram_with_bins(s0=200, mu=0.0005, sigma=0.005, n=24, T=30, num_paths=100)

# Example usage:
# simulate_gbm_paths_plotly_with_histogram(s0=100, mu=0.05, sigma=0.2, n=24, T=30, num_paths=5)


st.write("""

Awesome! We've got a nice distribution that shows the different outcomes of our stock series.

3. Figure out how much the option is worth for each price

Let's do it again, and clearly mark the 'profitable' and 'unprofitable' zones: or where the price goes above the strike price.

For now, we'll set the strike price to be 210.""")

def simulate_gbm_paths_plotly_histogram_with_bins_and_color(s0, mu, sigma, n=24, T=30, num_paths=1000, num_bins=20, strike_threshold=200):
    dt = 1/n
    t = np.linspace(0, T, n*T+1)
    S = np.zeros((num_paths, n*T+1))
    
    for i in range(num_paths):
        W = np.random.standard_normal(size=n*T+1)
        W = np.cumsum(W)*np.sqrt(dt)
        X = (mu-0.5*sigma**2)*t + sigma*W
        S[i,:] = s0*np.exp(X)
    
    # Calculate end values
    end_values = S[:, -1]
    
    # Calculate histogram data
    hist_values, bin_edges = np.histogram(end_values, bins=num_bins)
    
    # Create subplots with one row and two columns
    fig = make_subplots(rows=1, cols=2, subplot_titles=('GBM Paths', 'End Value Histogram'), column_widths=[0.7, 0.3])
    
    # Add GBM paths to the first subplot
    for i in range(num_paths):
        fig.add_trace(go.Scatter(x=t, y=S[i,:], mode='lines', name=f'Path {i+1}'), row=1, col=1)

    colors_strike = ['red' if x < strike_threshold else 'green' for x in bin_edges[:-1]]
    
    # Add a bar chart with bins and counts to the second subplot
    fig.add_trace(go.Bar(y=bin_edges[:-1], x=hist_values, orientation='h', marker_color=colors_strike, name='End Values'), row=1, col=2)
    
    # Update layout
    fig.update_layout(
        title='Simulated Stock Paths and Colored Expiration Price Distribution',
        xaxis_title='Counts',
        yaxis_title='Price',
        xaxis2=dict(domain=[0.75, 1.0]),
        yaxis2=dict(anchor='x2'),
        showlegend=False,  # Set to False to avoid legend duplication
        width=1000,
        height=500,
    )
    
    st.plotly_chart(fig)

    return end_values, strike_threshold


end_prices, strike_value = simulate_gbm_paths_plotly_histogram_with_bins_and_color(s0=200, mu=0.0005, sigma=0.005, n=24, T=30, num_paths=100, strike_threshold=210)

st.write("""

4. Find the average value of the option based on the probability distribution of prices

Let's not look at the calculation exactly here, since it would be a bit long, but the price would be: """)

def call_option_asset(end_values, strike_value):
    payoffs = end_values - strike_value
    payoffs = np.clip(payoffs, 0, None)

    st.latex(payoffs.mean())
    return payoffs.mean()

call_option_asset(end_prices, strike_value)

st.write(""" 

### Price your own options! 

There's a bunch of parameters here that can change the distribution and the final price a lot, here's your chance to get a feel for it!

Start by playing around with one at a time, and then observe the relationships between them:

Some questions to answer: 

How does the option value usually change as a function of the current price?

How does the option value usually change as a function of the strike price?

How does the option value usually change as a function of the time to expiry?

How does the option value usually change as a function of the stock's volatility?

""")

st.write("""Current Price (what price is the stock at right now?)""")

s0_input = st.slider(
    'Select the price the stock is currently at!',
    100, 1000, 200)


st.write("""Strike Value (what price do we get the option to buy the stock at?)""")

strike_val_input = st.slider(
    'Select the strike price of the option!',
    int(s0_input*0.8), int(s0_input*1.2), s0_input)

st.write("""Time to Expiry (how many days until the option expires?)""")

time_to_expiry_input = st.slider(
    'Select the amount of days until the option expires!',
    1, 90, 30)

# st.write("""Stock Drift (does it tend to go up or down?)""")
# mu_input = st.slider(
#     'Select how much the stock trends up or down!',
#     -25, 25, 5)

st.write("""Stock Volatility (how wiggly are the price movements?)""")

sigma_input = st.slider(
    'Select how volatile the stock is!',
    0, 25, 5)

end_prices_interactive, strike_val_input = simulate_gbm_paths_plotly_histogram_with_bins_and_color(s0=s0_input, 
                                                                                                   mu=0.0005, sigma=sigma_input/1e3, 
                                                                                                   n=24, T=time_to_expiry_input, 
                                                                                                   num_paths=200, 
                                                                                                   strike_threshold=strike_val_input)

call_option_asset(end_prices_interactive, strike_val_input)

st.write("""

### Lessons from Histograms

What did you learn? 

Well, you should've noticed the following

1. Option Price Depends on the Current Price

2. Option Price Depends on the Strike Price

3. Option Price Depends on the Time to Expiry

4. Option Price Depends on the Volatility of a Stock

Intuitively, all of these should make sense!

TODO: make these sentences better

A better discount (or lower relative price to buy an asset at) should mean that a coupon is worth more than another coupon, because it's profitability threshold lower down on the range of prices possible, so the probability of it ending up profitable is higher!

A coupon that expires later than another one should be more valuable than one that expires later, since price has more time to move around, causing the probability of it ending up profitable to be higher!

A coupon that is for an asset that has a very jumpy price should be more valuable, because the range of prices it can reach is wider, so the probability of it ending up profitable is higher!

These values are known as **Option Greeks**

### What are Option Greeks? 

Option greeks are just greek letters that represent how an option's price changes as some other variable changes

The basic ones you need to know about are:

Theta, Delta, and Vega:

**Theta** is the time value of an option: since more time to expiry increases the width of the ending price distribution, so the probability of ending above the strike is higher

**Delta** is the option's sensitivity to the stock price movement: as a stock goes up, its probability of ending above the strike is higher

**Vega** is the option's sensitivity to volatility: as a stock gets more volatile, the width of its distribution increases, so the probability of ending above the strike is higher

### Option Prices as a function of Volatility

Notice how, at any given time, we will always know:
- the option's strike price
- the option's days to expiry
- the stock's current price

But what we don't know is:
- the stock's volatility

If we know an option's volatility, we can work out what the price of the option should be. 

Vice versa, if we know the price of an option, we can work out the 'implied volatility' of an option. 

### Why and how do we trade volatility?

Unlike in the model shown above, volatility is not constant over time. 

One obvious example of stock volatility changing is news announcements. Apple's share price is likely to be more volatile when a new iPhone releases, than when nothing big and interesting is happening with the company. 

While the market has an implied volatility that we can infer from the option's price, what actually happens might be different. 

We call the volatility that actually happens 'realized volatility'. 

- If we think a stock's 'realized volatility' will be higher than the market's 'implied volatility' derived from the option price, we should buy the option
  - This is because if the volatility that ends up occurring is higher than what the market predicted, the option is more valuable on average, so we make money!
  - Circling back to our coupon example, this means that we should buy coupons from Nike only if we think they're understimating how much their shoes might fluctuate in value. 
  - We should only agree to the deal with our coworker if we think she's underestimating how much the handbag might fluctuate in value. 

- Likewise, if we think a stock's 'realized volatility' will be lower than market's 'implied volatility' derived from the option price, we should sell the option
  - Now, if the volatility that ends up occurring is lower than what the market predicted, the option will be less valuable on average, so we make money!
  - Nike probably sold the coupons because they thought that we'd overestimate the volatility of the shoe price
  - Our coworker probably made the deal with us because she thought we'd overestimate the volatility of the handbag

This is why options are so intertwined with our beliefs about the volatility of a stock: their price is a direct expression of what the market expects a stock's volatility to be. 

### Other Stuff

This explainer is a work in progress! Please send feedback to: 

### Some FAQ I didn't cover:

#### How do I sell an option I don't have? 

Remember how Nike gave us coupons, and our coworker offered us a deal? 

Just like how you can buy these contracts, you can write one up for someone else to buy!

There are times where you might want to be the one writing the contract, usually when you think that someone else is overestimating future 'realized volatility' versus your expectation

#### What if I'm right about volatility, but wrong about the price movement? 

This is a bit out of scope but if you think about it, you would want to offset the risk of the stock moving somehow. 

If you're long a put option, then your option doesn't just make money when realized volatility is higher than implied, you also make money when the stock goes down. But this means you'll also lose money if the stock goes up. 

To offset this risk that comes from the direction of the stock movement, you'll likely want to buy enough shares to offset the price change of your option.

The effect 'Delta' that we explored earlier, the option's sensitivity to price change in the underlying stock, is the effect we want to cancel out. 

If an option has 0.5 delta, then it moves 50 cents for each dollar movement in the underlying stock.

So if your option has 0.5 delta, and moves 50 cents for every dollar movement in the underlying stock, you probably want to buy 50 shares of the stock. (this is because a stock option multiplier is 100 shares, 100 x 0.5 = 50)

This means, in order to purely trade volatility, we can 'delta hedge' our risk due to the underlying stock's movement by buying shares (or selling them) 

MAYBE: 
put call parity

second order greeks

""")


