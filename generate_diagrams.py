import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs('report_assets', exist_ok=True)

# -------------------------------------------------------------------------
# 1. GENERATE ERD (Entity Relationship Diagram)
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
ax.set_xlim(0, 120)
ax.set_ylim(0, 90)
ax.axis('off')

# Title
ax.text(60, 86, "CRAVEHUB - ENTITY RELATIONSHIP DIAGRAM (ERD)", 
        fontsize=16, fontweight='bold', ha='center', color='#1E1B4B')
ax.text(60, 83, "Relational Database Schema (MySQL / SQLite)", 
        fontsize=10, ha='center', color='#475569', style='italic')

def draw_table(ax, x, y, title, columns, width=32, row_h=3.2):
    total_h = (len(columns) + 1) * row_h
    # Main box
    rect = patches.FancyBboxPatch((x, y - total_h), width, total_h, 
                                  boxstyle="round,pad=0.2", 
                                  fc="#FFFFFF", ec="#4338CA", lw=1.5)
    ax.add_patch(rect)
    # Header box
    hdr = patches.Rectangle((x, y - row_h), width, row_h, 
                            fc="#4338CA", ec="#4338CA")
    ax.add_patch(hdr)
    ax.text(x + width/2, y - row_h/2 - 0.4, title, 
            fontsize=10, fontweight='bold', color='white', ha='center', va='center')
    
    # Columns
    cur_y = y - row_h - 1.8
    for col in columns:
        prefix = "PK " if col.startswith("PK") else ("FK " if col.startswith("FK") else "• ")
        clean_col = col.replace("PK ", "").replace("FK ", "")
        
        # Color coding
        if "PK" in col:
            color = "#B91C1C"
            fw = 'bold'
        elif "FK" in col:
            color = "#1D4ED8"
            fw = 'bold'
        else:
            color = "#1E293B"
            fw = 'normal'
            
        ax.text(x + 1.2, cur_y, prefix, fontsize=8, fontweight='bold', color=color, va='center')
        ax.text(x + 4.5, cur_y, clean_col, fontsize=8, fontweight=fw, color=color, va='center')
        cur_y -= row_h

# Draw Tables
# 1. USERS
draw_table(ax, 5, 78, "USERS", [
    "PK user_id (INT)",
    "name (VARCHAR)",
    "email (VARCHAR, UNIQUE)",
    "phone (VARCHAR, UNIQUE)",
    "password (VARCHAR)",
    "role (ENUM: Customer, Admin, ...)",
    "created_at (TIMESTAMP)"
])

# 2. CATEGORIES
draw_table(ax, 5, 45, "CATEGORIES", [
    "PK category_id (INT)",
    "name (VARCHAR)"
])

# 3. MENU_ITEMS
draw_table(ax, 45, 48, "MENU_ITEMS", [
    "PK item_id (INT)",
    "FK category_id (INT)",
    "name (VARCHAR)",
    "description (TEXT)",
    "price (DECIMAL)",
    "image_url (TEXT)",
    "is_available (BOOLEAN)"
])

# 4. ORDERS
draw_table(ax, 45, 82, "ORDERS", [
    "PK order_id (INT)",
    "FK user_id (INT)",
    "FK delivery_user_id (INT)",
    "total_amount (DECIMAL)",
    "status (ENUM)",
    "delivery_address (TEXT)",
    "otp_code (VARCHAR)",
    "payment_method (VARCHAR)",
    "payment_status (VARCHAR)",
    "created_at (TIMESTAMP)"
])

# 5. ORDER_ITEMS
draw_table(ax, 85, 82, "ORDER_ITEMS", [
    "PK order_item_id (INT)",
    "FK order_id (INT)",
    "FK item_id (INT)",
    "quantity (INT)",
    "unit_price (DECIMAL)"
])

# 6. PAYMENTS
draw_table(ax, 85, 45, "PAYMENTS", [
    "PK payment_id (INT)",
    "FK order_id (INT)",
    "amount (DECIMAL)",
    "payment_method (VARCHAR)",
    "upi_id (VARCHAR)",
    "transaction_id (VARCHAR)",
    "status (VARCHAR)"
])

# Draw Relationship Lines
def draw_line(x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#4338CA", lw=1.5, ls="--"))
    if label:
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my + 1, label, fontsize=7.5, color="#4338CA", fontweight='bold', ha='center')

# USERS -> ORDERS (1 : N)
draw_line(37, 65, 45, 65, "1 : N (places)")
# CATEGORIES -> MENU_ITEMS (1 : N)
draw_line(37, 38, 45, 38, "1 : N (contains)")
# ORDERS -> ORDER_ITEMS (1 : N)
draw_line(77, 72, 85, 72, "1 : N (has)")
# MENU_ITEMS -> ORDER_ITEMS (1 : N)
draw_line(65, 48, 85, 62, "1 : N (included in)")
# ORDERS -> PAYMENTS (1 : 1)
draw_line(65, 50, 85, 35, "1 : 1 (generates)")

plt.tight_layout()
plt.savefig("report_assets/erd_diagram.png", bbox_inches='tight', dpi=300)
plt.close()
print("ERD diagram generated successfully!")

# -------------------------------------------------------------------------
# 2. GENERATE DFD LEVEL 0 (Context Diagram)
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 60)
ax.axis('off')

ax.text(50, 56, "DATA FLOW DIAGRAM (DFD) - LEVEL 0", fontsize=15, fontweight='bold', ha='center', color='#1E1B4B')
ax.text(50, 53, "CraveHub Context Level Diagram", fontsize=10, ha='center', color='#64748B')

# Center System Bubble
circle = patches.Circle((50, 28), 12, fc="#EDE9FE", ec="#6366F1", lw=2)
ax.add_patch(circle)
ax.text(50, 30, "0.0", fontsize=11, fontweight='bold', ha='center', color='#4338CA')
ax.text(50, 27, "CRAVEHUB\nFOOD SYSTEM", fontsize=10, fontweight='bold', ha='center', color='#1E1B4B')

def draw_entity(x, y, label):
    rect = patches.Rectangle((x, y), 20, 8, fc="#F8FAFC", ec="#0F172A", lw=1.5)
    ax.add_patch(rect)
    ax.text(x + 10, y + 4, label, fontsize=9, fontweight='bold', ha='center', va='center', color='#0F172A')

draw_entity(5, 40, "CUSTOMER")
draw_entity(5, 10, "DELIVERY\nPARTNER")
draw_entity(75, 40, "KITCHEN\nSTAFF")
draw_entity(75, 10, "ADMIN\nMANAGER")

# Arrows
def draw_flow(x1, y1, x2, y2, label, offset_y=1.5):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#4F46E5", lw=1.2))
    mx, my = (x1 + x2)/2, (y1 + y2)/2
    ax.text(mx, my + offset_y, label, fontsize=7, color="#312E81", fontweight='bold', ha='center')

draw_flow(25, 45, 40, 35, "Browse, Order & Pay")
draw_flow(40, 31, 25, 41, "Live Tracking & OTP", -2)

draw_flow(60, 35, 75, 45, "Order Dispatch")
draw_flow(75, 41, 60, 31, "Status: Ready", -2)

draw_flow(55, 20, 75, 15, "Analytics & Control")
draw_flow(75, 12, 55, 17, "Menu Updates", -2)

draw_flow(45, 20, 25, 15, "Assigned Deliveries")
draw_flow(25, 12, 45, 17, "OTP Handover Verified", -2)

plt.tight_layout()
plt.savefig("report_assets/dfd_level0.png", bbox_inches='tight', dpi=300)
plt.close()
print("DFD Level 0 diagram generated successfully!")

# -------------------------------------------------------------------------
# 3. GENERATE DFD LEVEL 1 (Subsystems & Data Stores)
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
ax.set_xlim(0, 110)
ax.set_ylim(0, 80)
ax.axis('off')

ax.text(55, 76, "DATA FLOW DIAGRAM (DFD) - LEVEL 1", fontsize=15, fontweight='bold', ha='center', color='#1E1B4B')
ax.text(55, 73, "Decomposition of CraveHub Main System Processes", fontsize=9.5, ha='center', color='#64748B')

def draw_proc(x, y, num, name):
    circ = patches.Circle((x, y), 6.5, fc="#F5F3FF", ec="#7C3AED", lw=1.5)
    ax.add_patch(circ)
    ax.text(x, y + 1.8, num, fontsize=8, fontweight='bold', color='#7C3AED', ha='center')
    ax.text(x, y - 1.2, name, fontsize=7.5, fontweight='bold', color='#1E1B4B', ha='center')

def draw_store(x, y, num, name):
    rect = patches.Rectangle((x, y), 24, 5, fc="#EEF2FF", ec="#4F46E5", lw=1)
    ax.add_patch(rect)
    ax.plot([x + 6, x + 6], [y, y + 5], color="#4F46E5", lw=1)
    ax.text(x + 3, y + 2.5, num, fontsize=7.5, fontweight='bold', color="#4F46E5", ha='center', va='center')
    ax.text(x + 15, y + 2.5, name, fontsize=8, fontweight='bold', color="#1E293B", ha='center', va='center')

# Processes
draw_proc(20, 60, "1.0", "Authentication\n& Profile")
draw_proc(55, 60, "2.0", "Menu & Cart\nManagement")
draw_proc(90, 60, "3.0", "Order & UPI\nPayment")
draw_proc(20, 25, "4.0", "Kitchen KDS\nPreparation")
draw_proc(55, 25, "5.0", "Delivery & OTP\nHandover")
draw_proc(90, 25, "6.0", "Analytics &\nReporting")

# Data Stores
draw_store(35, 42, "D1", "Users Store")
draw_store(72, 42, "D2", "Menu Store")
draw_store(35, 10, "D3", "Orders Store")
draw_store(72, 10, "D4", "Payments Store")

# Flow connections
def conn(x1, y1, x2, y2, lbl=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#6366F1", lw=1.2, ls="-"))
    if lbl:
        ax.text((x1+x2)/2, (y1+y2)/2 + 1, lbl, fontsize=6.5, color="#3730A3", ha='center', fontweight='bold')

conn(26.5, 60, 48.5, 60, "Session User")
conn(61.5, 60, 83.5, 60, "Checkout Items")
conn(20, 53.5, 35, 45, "User Creds")
conn(55, 53.5, 72, 45, "Menu Query")
conn(90, 53.5, 84, 15, "Tx Details")
conn(90, 53.5, 59, 15, "New Order")
conn(47, 15, 26, 25, "Ready Notification")
conn(55, 20, 55, 15, "Status Update")
conn(90, 20, 84, 13, "Sales Data")

plt.tight_layout()
plt.savefig("report_assets/dfd_level1.png", bbox_inches='tight', dpi=300)
plt.close()
print("DFD Level 1 diagram generated successfully!")
