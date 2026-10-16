import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs('report_assets', exist_ok=True)

def create_mockup(filename, title, elements_fn):
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=250)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 55)
    ax.axis('off')
    
    # Outer browser window frame
    window = patches.FancyBboxPatch((1, 1), 98, 53, boxstyle="round,pad=0.5", fc="#FFFFFF", ec="#CBD5E1", lw=1.5)
    ax.add_patch(window)
    
    # Title bar
    tbar = patches.Rectangle((1, 50), 98, 4, fc="#F1F5F9", ec="#CBD5E1")
    ax.add_patch(tbar)
    for i, c in enumerate(["#EF4444", "#F59E0B", "#10B981"]):
        dot = patches.Circle((3 + i*2.5, 52), 0.9, fc=c, ec=None)
        ax.add_patch(dot)
        
    ax.text(50, 52, f"CraveHub Platform -- {title}", fontsize=8.5, ha='center', va='center', color="#475569", fontweight='bold')
    
    elements_fn(ax)
    
    plt.tight_layout()
    plt.savefig(f"report_assets/{filename}", bbox_inches='tight', dpi=250)
    plt.close()
    print(f"Generated {filename}")

# 1. Login Snapshot
def draw_login(ax):
    box = patches.FancyBboxPatch((32, 8), 36, 40, boxstyle="round,pad=0.5", fc="#FFFFFF", ec="#DDD6FE", lw=1.5)
    ax.add_patch(box)
    ax.text(50, 44, "CRAVEHUB", fontsize=16, fontweight='bold', color="#6D28D9", ha='center')
    ax.text(50, 41, "Fresh - Fast - Delicious", fontsize=8.5, color="#64748B", ha='center')
    
    # Tabs
    t1 = patches.Rectangle((34, 35), 15, 3.5, fc="#F5F3FF", ec="#7C3AED", lw=1.2)
    t2 = patches.Rectangle((51, 35), 15, 3.5, fc="#FFFFFF", ec="#E2E8F0")
    ax.add_patch(t1); ax.add_patch(t2)
    ax.text(41.5, 36.7, "Sign In", fontsize=8, fontweight='bold', color="#6D28D9", ha='center', va='center')
    ax.text(58.5, 36.7, "Create Account", fontsize=8, color="#64748B", ha='center', va='center')
    
    # Inputs
    ax.text(34, 32, "Email Address", fontsize=7.5, fontweight='bold', color="#1E293B")
    inp1 = patches.Rectangle((34, 27), 32, 3.8, fc="#FFFFFF", ec="#DDD6FE", lw=1)
    ax.add_patch(inp1)
    ax.text(36, 28.9, "customer@cravehub.com", fontsize=7.5, color="#0F172A", va='center')
    
    ax.text(34, 24.5, "Password", fontsize=7.5, fontweight='bold', color="#1E293B")
    inp2 = patches.Rectangle((34, 19.5), 32, 3.8, fc="#FFFFFF", ec="#DDD6FE", lw=1)
    ax.add_patch(inp2)
    ax.text(36, 21.4, "**********", fontsize=8, color="#0F172A", va='center')
    
    # Submit Button
    btn = patches.Rectangle((34, 12.5), 32, 4.5, fc="#7C3AED", ec=None)
    ax.add_patch(btn)
    ax.text(50, 14.7, "SIGN IN TO CRAVEHUB", fontsize=8.5, fontweight='bold', color="#FFFFFF", ha='center', va='center')

create_mockup("snapshot_login.png", "Authentication & User Portal", draw_login)

# 2. Customer Showcase Snapshot
def draw_customer(ax):
    # Sidebar
    sb = patches.Rectangle((1, 1), 20, 49, fc="#FAF5FF", ec="#EDE9FE")
    ax.add_patch(sb)
    ax.text(11, 46, "CRAVEHUB", fontsize=11, fontweight='bold', color="#6D28D9", ha='center')
    ax.text(11, 43, "Role: Gourmet Foodie", fontsize=6.5, color="#475569", ha='center')
    ax.text(11, 38, "[2 Items in Cart]", fontsize=7, color="#16A34A", fontweight='bold', ha='center')
    
    # Hero Banner
    hero = patches.FancyBboxPatch((23, 34), 74, 14, boxstyle="round,pad=0.3", fc="#7C3AED", ec=None)
    ax.add_patch(hero)
    ax.text(26, 44, "FAST 30-MIN EXPRESS DELIVERY  |  4.9 GOURMET CHEFS  |  100% FRESH & HYGIENIC", fontsize=6.5, color="#DDD6FE", fontweight='bold')
    ax.text(26, 39.5, "Craving Something Delicious Today?", fontsize=12, fontweight='bold', color="#FFFFFF")
    ax.text(26, 36.2, "Order authentic chef-prepared delicacies with real-time live tracking & instant UPI payment!", fontsize=7, color="#EDE9FE")
    
    # Food Cards
    dishes = [("Royal Butter Chicken", "Rs 320", "Main Course"), 
              ("Tandoori Paneer Tikka", "Rs 240", "Starters"), 
              ("Hyderabadi Biryani", "Rs 290", "Main Course")]
    for i, dish in enumerate(dishes):
        cx = 24 + i*25
        card = patches.FancyBboxPatch((cx, 8), 23, 23, boxstyle="round,pad=0.3", fc="#FFFFFF", ec="#EDE9FE", lw=1.2)
        ax.add_patch(card)
        # Dish image mockup
        img_mock = patches.Rectangle((cx + 1, 19), 21, 11, fc="#EEF2FF")
        ax.add_patch(img_mock)
        ax.text(cx + 11.5, 24.5, "[Food Item Image]", fontsize=7.5, color="#6366F1", ha='center')
        ax.text(cx + 2, 16.5, dish[0], fontsize=8, fontweight='bold', color="#0F172A")
        ax.text(cx + 2, 14, "Rating: 4.8 / 5.0", fontsize=6.5, color="#D97706")
        # Price badge
        pbadge = patches.Rectangle((cx + 14, 14.5), 7.5, 3, fc="#7C3AED")
        ax.add_patch(pbadge)
        ax.text(cx + 17.7, 16, dish[1], fontsize=7, fontweight='bold', color="#FFFFFF", ha='center', va='center')
        # Add button
        add_btn = patches.Rectangle((cx + 2, 9.5), 19, 3.2, fc="#7C3AED")
        ax.add_patch(add_btn)
        ax.text(cx + 11.5, 11.1, "+ Add to Order", fontsize=7, fontweight='bold', color="#FFFFFF", ha='center', va='center')

create_mockup("snapshot_customer.png", "Customer Showcase & Menu Grid", draw_customer)

# 3. Live Tracking Snapshot
def draw_tracking(ax):
    cont = patches.FancyBboxPatch((15, 6), 70, 42, boxstyle="round,pad=0.5", fc="#FFFFFF", ec="#DDD6FE", lw=1.5)
    ax.add_patch(cont)
    ax.text(50, 44, "Order #ORD-1049 -- Live Order Tracking", fontsize=12, fontweight='bold', color="#1E1B4B", ha='center')
    ax.text(50, 41, "Address: 402, Green Park Residency, Pune  |  Amount: Rs 588.00 (UPI Paid)", fontsize=7.5, color="#64748B", ha='center')
    
    # 5-Step tracker line
    ax.plot([25, 75], [33, 33], color="#7C3AED", lw=3)
    steps = [("Order Placed", 25, True), 
             ("Preparing", 37.5, True), 
             ("Food Ready", 50, True), 
             ("On The Way", 62.5, True), 
             ("Delivered", 75, False)]
    for name, sx, active in steps:
        scol = "#7C3AED" if active else "#CBD5E1"
        pt = patches.Circle((sx, 33), 2.2, fc="#FFFFFF", ec=scol, lw=2)
        ax.add_patch(pt)
        ax.text(sx, 33, "[OK]" if active else "[ ]", fontsize=6, fontweight='bold', color=scol, ha='center', va='center')
        ax.text(sx, 27.5, name, fontsize=7, fontweight='bold' if active else 'normal', color=scol, ha='center')
        
    # OTP Box
    otp_box = patches.FancyBboxPatch((26, 11), 48, 12, boxstyle="round,pad=0.3", fc="#FEF3C7", ec="#F59E0B", lw=1.2)
    ax.add_patch(otp_box)
    ax.text(50, 19.5, "Delivery Verification OTP Code: 4 8 2 1", fontsize=10.5, fontweight='bold', color="#92400E", ha='center')
    ax.text(50, 16.5, "Provide this 4-digit code to the delivery executive at handover.", fontsize=7.5, color="#78350F", ha='center')
    ax.text(50, 13.5, "Assigned Partner: Rahul Sharma (Phone: 9900112233)", fontsize=7.5, fontweight='bold', color="#1E293B", ha='center')

create_mockup("snapshot_tracking.png", "5-Step Live Tracking & OTP Handover", draw_tracking)

# 4. Analytics Snapshot
def draw_analytics(ax):
    for i, (lbl, val) in enumerate([("Total Revenue", "Rs 1,42,850.00"), ("Total Orders", "428 Orders"), ("Average Order Value", "Rs 333.76")]):
        bx = 6 + i*31
        card = patches.FancyBboxPatch((bx, 38), 28, 10, boxstyle="round,pad=0.3", fc="#FAF5FF", ec="#DDD6FE", lw=1.2)
        ax.add_patch(card)
        ax.text(bx + 14, 45, lbl, fontsize=7.5, color="#6D28D9", fontweight='bold', ha='center')
        ax.text(bx + 14, 40.5, val, fontsize=11, fontweight='bold', color="#1E1B4B", ha='center')
        
    c1 = patches.Rectangle((6, 8), 43, 26, fc="#FFFFFF", ec="#E2E8F0")
    ax.add_patch(c1)
    ax.text(27.5, 31, "Daily Revenue Trend (Last 7 Days)", fontsize=8, fontweight='bold', color="#1E293B", ha='center')
    ax.plot([10, 17, 24, 31, 38, 45], [13, 19, 16, 24, 22, 28], color="#7C3AED", lw=2, marker='s')
    
    c2 = patches.Rectangle((52, 8), 43, 26, fc="#FFFFFF", ec="#E2E8F0")
    ax.add_patch(c2)
    ax.text(73.5, 31, "Top Selling Dishes by Quantity", fontsize=8, fontweight='bold', color="#1E293B", ha='center')
    dishes = [("Butter Chicken", 25), ("Paneer Tikka", 20), ("Biryani Special", 18), ("Garlic Naan", 14)]
    for j, (dn, q) in enumerate(dishes):
        ax.barh(27 - j*5, q, height=3, left=56, color="#6366F1")
        ax.text(57, 27 - j*5, dn, fontsize=6.5, color="#FFFFFF", fontweight='bold', va='center')

create_mockup("snapshot_analytics.png", "Executive Analytics & Reporting", draw_analytics)
