import streamlit as st
import random

# Function to calculate hedge bet, profit, and loss
def calculate_hedge(initial_odds, bet_amount, available_hedge_odds):
    if initial_odds <= 1 or bet_amount <= 0 or available_hedge_odds <= 1:
        return None, None, None, "❌ Invalid Input: Enter valid odds & bet amount."
    
    hedge_bet = (bet_amount * initial_odds) / available_hedge_odds
    total_bet = bet_amount + hedge_bet

    # Profit/loss calculation
    profit_if_first_wins = (bet_amount * initial_odds) - total_bet
    profit_if_second_wins = (hedge_bet * available_hedge_odds) - total_bet

    return hedge_bet, profit_if_first_wins, profit_if_second_wins, None

# Motivational Quotes for Win/Loss
win_quotes = [
    "You trusted your instincts, and they led you straight to victory!",
    "Success tastes even sweeter when it’s earned through smart decisions.",
    "Luck may have smiled on you, but skill sealed the deal.",
    "Winning isn’t just about luck—it’s about making the right call at the right time.",
]

loss_quotes = [
    "Losses are part of the journey—they teach us how to win better next time.",
    "Even champions lose sometimes. What matters is learning from it.",
    "Losing is temporary; giving up is permanent. Stay in the game!",
    "Even the pros don’t win all their bets. Dust yourself off and try again.",
]

# Streamlit UI Config (Set layout and remove top space)
st.set_page_config(page_title="Betting Hedge Calculator", page_icon="🎲", layout="wide")

# Remove extra space from the top
st.markdown(
    """
    <style>
    .stApp { margin-top: -80px; } /* Moves content up */
    .big-font { font-size:18px !important; }
    .profit-box { background-color: #D4EDDA; padding: 10px; border-radius: 10px; }
    .loss-box { background-color: #F8D7DA; padding: 10px; border-radius: 10px; }
    .info-box { background-color: #CCE5FF; padding: 10px; border-radius: 10px; }
    .centered { display: flex; justify-content: center; align-items: center; }
    </style>
    """, unsafe_allow_html=True
)

# Title (Now positioned at the very top)
st.markdown("<h2 style='text-align: center;'>🎲 Betting Hedge Calculator</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>💡 Find the optimal bet to minimize loss or secure profit.</p>", unsafe_allow_html=True)
st.markdown("---")

# Layout: Left (Betting Details) | Right (Optimal Strategy)
col1, col2 = st.columns([1, 1])  # Equal split

# Left Column: Betting Details
with col1:
    st.subheader("📌 Enter Betting Details")
    initial_odds = st.number_input("Your Placed Odds", min_value=0.0, step=0.01, placeholder="Enter Your Placed Odds", format="%.2f")
    bet_amount = st.number_input("Your Bet Amount (₹)", min_value=0, step=1, placeholder="Enter Your Bet Amount")
    available_hedge_odds = st.number_input("Available Opposite Odds", min_value=0.0, step=0.01, placeholder="Enter Available Odds", format="%.2f")

# Live Calculation (Only Show Results If Input Is Valid)
if initial_odds and bet_amount and available_hedge_odds:
    hedge_bet, profit_if_first_wins, profit_if_second_wins, error = calculate_hedge(initial_odds, bet_amount, available_hedge_odds)
    
    # Right Column: Optimal Strategy
    with col2:
        st.subheader("📊 Optimal Betting Strategy")
        
        if error:
            st.error(error)
        else:
            st.success(f"✅ **Place Hedge Bet:** ₹{round(hedge_bet, 2)} at {available_hedge_odds} odds")

            # Display Corrected Profit/Loss Metrics
            c1, c2 = st.columns(2)
            
            if profit_if_first_wins < 0:
                c1.metric(label="⚠️ Loss if First Bet Wins", value=f"₹{round(abs(profit_if_first_wins), 2)}")
            else:
                c1.metric(label="✅ Profit if First Bet Wins", value=f"₹{round(profit_if_first_wins, 2)}")

            if profit_if_second_wins < 0:
                c2.metric(label="⚠️ Loss if Second Bet Wins", value=f"₹{round(abs(profit_if_second_wins), 2)}")
            else:
                c2.metric(label="✅ Profit if Second Bet Wins", value=f"₹{round(profit_if_second_wins, 2)}")

            # Determine whether it's a loss or profit
            min_profit = min(profit_if_first_wins, profit_if_second_wins)

            if min_profit < 0:
                st.markdown(f'<div class="loss-box">⚠️ **Loss: ₹{round(abs(min_profit), 2)}**</div>', unsafe_allow_html=True)
                st.info(f"💬 *{random.choice(loss_quotes)}*")
            else:
                st.markdown(f'<div class="profit-box">💰 **Guaranteed Profit: ₹{round(min_profit, 2)}**</div>', unsafe_allow_html=True)
                st.info(f"🎉 *{random.choice(win_quotes)}*")

st.markdown("---")
st.caption("🔹 Adjust odds & amounts to see updated results instantly.")
