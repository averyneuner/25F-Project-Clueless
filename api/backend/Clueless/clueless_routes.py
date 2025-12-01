from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

analytics = Blueprint('analytics', __name__)
business = Blueprint('business', __name__)
customer = Blueprint('customer', __name__)
general = Blueprint('general', __name__)


# ----------- Admin/general Routes -----------

@general.route("/outfits", methods=["POST"])
def create_outfit():
    try:
        data = request.get_json()
        required_fields = ["nickname", "description"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        cursor = db.get_db().cursor()
        cursor.execute("SELECT MAX(OutfitId) FROM Outfit")
        res = cursor.fetchone()
        new_id = (res['MAX(OutfitId)'] or 400) + 1
        query = """
        INSERT INTO Outfit (OutfitID, Nickname, Description)
        VALUES (%s, %s, %s)
        """
        cursor.execute(
            query,
            (
                new_id,
                data["nickname"],
                data["description"]
            )
        )
        db.get_db().commit()
        cursor.close()
        return (
            jsonify({"message": "Outfit created successfully"}),
            201,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@general.route("/outfits", methods=["GET"])
def search_outfits():
    try:
        cursor = db.get_db().cursor()
        aesthetic = request.args.get('aesthetic')
        
        cursor.execute("""
             SELECT o.OutfitID, o.Nickname, o.Description, a.Name AS AestheticName
             FROM Outfit o
             JOIN OutfitMatchedAesthetic oma ON o.OutfitID = oma.OutfitID
             JOIN Aesthetic a ON oma.AestheticID = a.AestheticID
             WHERE a.Name = %s
        """, (aesthetic,))
        outfits = cursor.fetchall()
        cursor.close()
        return jsonify(outfits), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@general.route("/outfits", methods=["DELETE"])
def delete_outfit():
    try:
        cursor = db.get_db().cursor()
        closet_id = request.args.get('closet_id')
        outfit_id = request.args.get('outfit_id')
        cursor.execute("""
            SELECT cc.NickName, o.Nickname
            FROM CustomerClosetOutfits cco
            JOIN CustomerCloset cc ON cco.ClosetID = cc.ClosetID
            JOIN Outfit o ON cco.OutfitID = o.OutfitID
            WHERE cco.ClosetID = %s AND cco.OutfitID = %s
            LIMIT 1
        """, (closet_id, outfit_id))
        info = cursor.fetchone()
        cursor.execute("""
            DELETE FROM CustomerClosetOutfits WHERE ClosetID = %s AND OutfitID = %s
        """, (closet_id, outfit_id))
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Outfit removed", "deleted_data": info}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@general.route("/items", methods=["POST"])
def create_clothing_item():
    try:
        data = request.get_json()
        required_fields = ["image", "name", "category", "price", "size", "rating"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        cursor.execute("SELECT MAX(ItemId) FROM ClothingItem")
        res = cursor.fetchone()
        new_id = (res['MAX(ItemId)'] or 400) + 1
        cursor = db.get_db().cursor()
        query = """
        INSERT INTO ClothingItem 
        (ItemID, ImageAddress, Name, Category, Price, Size, QualityRating, OutdatedFlag, PopularityPercentage)
        VALUES (%s, %s, %s, %s, %s, %s, %s, False, 0.00)
        """
        cursor.execute(
            query,
            (
                new_id,
                data["image"],
                data["name"],
                data["category"],
                data["price"],
                data["size"],
                data["rating"]
            )
        )
        db.get_db().commit()
        cursor.close()
        return (
           jsonify({"message": "Item created successfully"}),
            201,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@general.route("/items", methods=["GET"])
def search_items():
    try:
        cursor = db.get_db().cursor()
        aesthetic = request.args.get('aesthetic')
        cursor.execute("""
            SELECT ci.ItemID, ci.Name, ci.Price, ci.PopularityPercentage
            FROM CustomerCloset cc
            JOIN CustomerClosetOutfits cco ON cc.ClosetID = cco.ClosetID
            JOIN OutfitMatchedAesthetic oma ON cco.OutfitID = oma.OutfitID
            JOIN Aesthetic a ON oma.AestheticID = a.AestheticID
            JOIN ClothingItemMatchedAesthetic cima ON a.AestheticID = cima.AestheticID
            JOIN ClothingItem ci ON cima.ClothingItemID = ci.ItemID
            WHERE a.Name = %s
            ORDER BY ci.PopularityPercentage DESC
        """, (aesthetic,))
        items = cursor.fetchall()
    
        cursor.close()
        return jsonify(items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@general.route("/admin/users", methods=["GET"])
def get_admin_users():
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT c.CustomerID, c.FirstName, c.LastName, c.EmailAddress, 
                   COUNT(DISTINCT cc.ClosetID) AS TotalClosets
            FROM Customer c
            LEFT JOIN CustomerCloset cc ON c.CustomerID = cc.CustomerID
            GROUP BY c.CustomerID, c.FirstName, c.LastName, c.EmailAddress
            ORDER BY c.CustomerID
        """)
        users = cursor.fetchall()
        cursor.close()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@general.route("/admin/logs", methods=["GET"])
def get_admin_logs():
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT bn.Status AS BusinessStatus, s.IssueLogs as Issues
            FROM `System` s
            JOIN BusinessNotification bn ON s.BusinessNotifID = bn.NotificationID
        """)
        business_logs = cursor.fetchall()
        cursor.execute("""
            SELECT * FROM `System` s
            JOIN TechTeam t ON s.SystemID = t.SystemID
            WHERE t.Name = 'Jenna Kim'
        """)
        tech_logs = cursor.fetchall()

        cursor.close()
        return jsonify({"business_logs": business_logs, "tech_logs": tech_logs}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------- Analytics Routes -----------

@analytics.route("/analytics/trend", methods=["GET"])
def get_trends():
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT Name, PopularityPercent, Description
            FROM Aesthetic
            ORDER BY PopularityPercent;
        """)
        trends = cursor.fetchall()
        cursor.close()
        return jsonify(trends), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@analytics.route("/analytics/items", methods=["GET"])
def get_item_analytics():
    try:
        cursor = db.get_db().cursor()
        ownable = """
            SELECT b.CompanyName, c.Name, c.ImageAddress
            FROM Customer cu
            JOIN CustomerCloset cc ON cu.CustomerID = cc.CustomerID
            JOIN CustomerClosetClothingItems ci ON cc.ClosetID = ci.ClosetID
            JOIN ClothingItem c ON ci.ClothingItemID = c.ItemID
            JOIN BusinessInventoryItemStorage biis ON c.ItemID = biis.ItemID
            JOIN BusinessInventory bi ON biis.InventoryID = bi.InventoryID
            JOIN Business b ON bi.CompanyID = b.CompanyID
            ORDER BY c.PopularityPercentage DESC;
        """
        cursor.execute(ownable)
        most_owned = cursor.fetchall()
        wearable = """
            SELECT ci.Name as ClothingItemName
            FROM CustomerClosetClothingItems cci
            JOIN ClothingItem ci ON cci.ClothingItemID = ci.ItemID
            JOIN BusinessInventoryItemStorage bs ON ci.ItemID = bs.ItemID
            JOIN BusinessInventory bi ON bs.InventoryID = bi.InventoryID
            JOIN Business b ON bi.CompanyID = b.CompanyID
            WHERE b.CompanyID = 01
            GROUP BY ci.ItemID
            ORDER BY SUM(cci.NumberOfWears) DESC; 
        """
        cursor.execute(wearable)
        most_worn = cursor.fetchall() 
        cursor.close()
        return jsonify({"most_owned": most_owned, "most_worn": most_worn}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analytics.route("/analytics/demand", methods=["GET"])
def get_demand_analytics():
    try:
        cursor = db.get_db().cursor()
        query = """
            SELECT c.Name, COUNT(w.ItemID) as total_wishlists
            FROM ClothingItem c
            JOIN CustWishListClothingItem cwi ON c.ItemID = cwi.ClothingItemID
            GROUP BY c.Name
            ORDER BY total_wishlists DESC
            LIMIT 10
        """
        cursor.execute(query)
        demand_data = cursor.fetchall()
        cursor.close()
        return jsonify(demand_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# ----------- Business Routes -----------

@business.route("/business/<int:business_id>/notifications", methods=["POST"])
def post_business_notification(business_id):
    try:
        data = request.get_json()
        required_fields = ["message"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        cursor = db.get_db().cursor()
        cursor.execute("SELECT MAX(NotificationID) FROM BusinessNotification")
        res = cursor.fetchone()
        new_id = (res['MAX(NotificationID)'] or 400) + 1
        query = """
        INSERT INTO BusinessNotification (NotificationID, Message, Status, CompanyID)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                new_id,
                data["message"],
                data.get("status", "Sent"),
                business_id
            )
        )
        db.get_db().commit()
        cursor.close()
        return (
            jsonify({"message": "Notification sent successfully", "id": new_id}),
            201,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@business.route("/business/<int:business_id>/notifications", methods=["GET"])
def get_business_notifications(business_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT bn.NotificationID, bn.Message, bn.Status, b.CompanyID, b.CompanyName, b.ContactEmail
            FROM BusinessNotification bn
            JOIN Business b ON bn.CompanyID = b.CompanyID
            WHERE b.CompanyID = %s
            ORDER BY bn.Status, b.CompanyName
        """, (business_id,))
        notifications = cursor.fetchall()
        cursor.close()
        return jsonify(notifications), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@business.route("/business/<int:business_id>/notifications", methods=["DELETE"])
def delete_business_notification(business_id):
    try:
        cursor = db.get_db().cursor()
        notif_id = request.args.get('notification_id')
        cursor.execute("""
            DELETE FROM BusinessNotification 
            WHERE NotificationID = %s AND CompanyID = %s
        """, (notif_id, business_id))
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Notification removed"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@business.route("/business/<int:business_id>/inventory/<int:inventory_id>/item/<int:item_id>", methods=["POST"])
def add_business_inventory_item(business_id, inventory_id, item_id):
    try:
        data = request.get_json()
        required_fields = ["EthicallySourcedFlag", "QuantityInStock"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        cursor = db.get_db().cursor()
        cursor.execute("SELECT MAX(ItemId) FROM BusinessInventoryItemStorage")
        res = cursor.fetchone()
        bridge_id = (res['MAX(ItemId)'] or 400) + 1
        cursor = db.get_db().cursor()
        cursor.execute("SELECT InventoryID FROM BusinessInventory WHERE CompanyID = %s", (business_id,))
        inv_row = cursor.fetchone()
        if not inv_row: 
            return jsonify({"error": "No inventory found"}), 404       
        cursor.execute("""
            INSERT INTO BusinessInventoryItemStorage 
            (ItemID, InventoryID, EthicallySourcedFlag, UnitsSold, QuantityInStock, ClothingItemID)
            VALUES (%s, %s, TRUE, 0.0, 0.0, %s)
        """, (bridge_id, data["EthicallySourcedFlage"], 0.0, data["QuantityInStock"], item_id))
        db.get_db().commit()
        cursor.close()
        jsonify({"message": "Item added to inventory successfully", "storage_id": bridge_id}),
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Resource: /business/{business id}/inventory/{item id}
# Verb: GET
@business.route("/business/<int:business_id>/inventory/<int:item_id>", methods=["GET"])
def get_business_inventory_item(business_id, item_id):
   try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT CI.ItemID, CI.Name, CI.Category, CI.Price, BIIS.UnitsSold, BIIS.QuantityInStock
            FROM BusinessInventoryItemStorage BIIS
            JOIN ClothingItem CI ON BIIS.ClothingItemID = CI.ItemID
            JOIN BusinessInventory BI ON BIIS.InventoryID = BI.InventoryID
            WHERE BI.CompanyID = %s AND CI.ItemID = %s
        """, (business_id, item_id))
        item = cursor.fetchone()
        cursor.close()
        return jsonify(item), 200
   except Exception as e:
        return jsonify({"error": str(e)}), 500

# Resource: /business/{business id}/inventory/{item id}
# Verb: PUT
@business.route("/business/<int:business_id>/inventory/<int:item_id>", methods=["PUT"])
def update_business_inventory_item(business_id, item_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            UPDATE BusinessInventoryItemStorage
            SET EthicallySourcedFlag = TRUE
            WHERE InventoryID IN (SELECT InventoryID FROM BusinessInventory WHERE CompanyID = %s)
            AND ClothingItemID = %s
        """, (business_id, item_id))
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Item marked as ethically sourced"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Resource: /business/{business id}/inventory/{item id}
# Verb: DELETE
@business.route("/business/<int:business_id>/inventory/<int:item_id>", methods=["DELETE"])
def delete_business_inventory_item(business_id, item_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            DELETE FROM BusinessInventoryItemStorage
            WHERE InventoryID IN (SELECT InventoryID FROM BusinessInventory WHERE CompanyID = %s)
            AND ClothingItemID = %s
        """, (business_id, item_id))
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Item removed from inventory"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@business.route("/business/<int:business_id>/wishlists/<int:wishlist_id>/item/<int:item_id>", methods=["POST"])
def add_business_inventory_item(business_id, wishlist_id, item_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT MAX(ItemID) FROM BusinessWishlistClothingItem")
        res = cursor.fetchone()
        bridge_id = (res['MAX(ItemID)'] or 400) + 1
        cursor = db.get_db().cursor()
        cursor.execute("SELECT WishlistID FROM BusinessWishlist WHERE CompanyID = %s", (business_id,))
        inv_row = cursor.fetchone()
        if not inv_row: 
            return jsonify({"error": "No inventory found"}), 404       
        cursor.execute("""
            INSERT INTO BusinessWishlistClothingItem (ItemID, WishlistID, ClothingItemID)
             VALUES (%s, %s, %s)
        """, (bridge_id, wishlist_id, item_id))
        db.get_db().commit()
        cursor.close()
        jsonify({"message": "Item added to wishlist successfully", "storage_id": bridge_id}),
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@business.route("/business/<int:business_id>/wishlists", methods=["DELETE"])
def delete_business_wishlist_item(business_id):
    try:
        cursor = db.get_db().cursor()
        item_id = request.args.get('item_id')
        cursor.execute("DELETE FROM BusinessWishlistClothingItem WHERE ItemID = %s", (item_id,))
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Item removed from wishlist"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

# ----------- Customer Routes -----------# 

@customer.route("/customer/<int:customer_id>/notifications", methods=["POST"])
def post_customer_notification(customer_id):
    try:
        data = request.get_json()
        required_fields = ["message"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        cursor = db.get_db().cursor()
        cursor.execute("SELECT MAX(NotificationID) FROM CustomerNotification")
        res = cursor.fetchone()
        new_id = (res['MAX(NotificationID)'] or 400) + 1
        query = """
            INSERT INTO CustomerNotification (NotificationID, Message, Status, CustomerID)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                new_id,
                data["message"],
                data.get("status", "Sent"),
                customer_id
            )
        )
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Notification sent successfully", "id": new_id}, 201)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customer.route("/customer/<int:customer_id>/notifications", methods=["GET"])
def get_customer_notifications(customer_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT cn.NotificationID, cn.Message, cn.Status, c.CustomerID
            FROM CustomerNotification cn
            JOIN Customer c ON cn.CustomerID = c.CustomerID
            WHERE c.CustomerID = %s
            ORDER BY cn.Status, cn.NotificationID
        """, (customer_id,))
        all_notifs = cursor.fetchall()
        cursor.close()
        return jsonify(all_notifs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customer.route("/customer/<int:customer_id>/closets", methods=["GET"])
def get_customer_closet(customer_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT c.ClosetID, ci.Name AS ItemName, ci.Category, cci.NumberofWears, cci.AvailabilityStatus
            FROM CustomerCloset c
            JOIN CustomerClosetClothingItems cci ON c.ClosetID = cci.ClosetID
            JOIN ClothingItem ci ON cci.ClothingItemID = ci.ItemID
            WHERE c.CustomerID = %s
            ORDER BY ci.Category, ci.Name
        """, (customer_id,))
        items = cursor.fetchall()
        cursor.execute("""
            SELECT o.OutfitID, o.Nickname AS OutfitName, ci.Name AS ItemName
            FROM CustomerCloset cc
            JOIN CustomerClosetOutfits cco ON cc.ClosetID = cco.ClosetID
            JOIN Outfit o ON cco.OutfitID = o.OutfitID
            JOIN CustomerOutfitsOfClothingItems coci ON o.OutfitID = coci.OutfitID
            JOIN ClothingItem ci ON coci.ClothingItemID = ci.ItemID
            WHERE cc.CustomerID = %s
            ORDER BY o.OutfitID
        """, (customer_id,))
        outfits = cursor.fetchall()
        cursor.close()
        return jsonify({"items": items, "outfits": outfits}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customer.route("/customer/<int:customer_id>/closets/<int:closet_id>/item/<int:item_id>", methods=["POST"])
def add_closet_item(customer_id, closet_id, item_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT MAX(ItemId) FROM CustomerClosetClothingItems")
        res = cursor.fetchone()
        bridge_id = (res['MAX(ItemId)'] or 400) + 1
        cursor = db.get_db().cursor()
        cursor.execute("SELECT ClosetID FROM CustomerCloset WHERE CustomerID = %s", (customer_id,))
        inv_row = cursor.fetchone()
        if not inv_row: 
            return jsonify({"error": "No closet found"}), 404     
        cursor.execute("""
            INSERT INTO CustomerClosetClothingItems (ClothingItemID, ClothingItemID, ClosetID, NumberofWears, AvailabilityStatus)
            VALUES (%s, %s, %s, 0, TRUE)
        """, (bridge_id, item_id, closet_id))
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Item added to closet successfully", "storage_id": bridge_id}),201, 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customer.route("/customer/<int:customer_id>/closets/<int:closet_id>/outfit/<int:outfit_id>", methods=["POST"])
def add_closet_outfit(customer_id, outfit_id, closet_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT MAX(OutfitID) FROM CustomerClosetOutfits")
        res = cursor.fetchone()
        bridge_id = (res['MAX(OutfitID)'] or 400) + 1
        cursor = db.get_db().cursor()
        cursor.execute("SELECT ClosetID FROM CustomerCloset WHERE CustomerID = %s", (customer_id,))
        inv_row = cursor.fetchone()
        if not inv_row: 
            return jsonify({"error": "No closet found"}), 404     
        cursor.execute("""
            INSERT INTO CustomerClosetOutfits (ClosetID, OutfitID)
            VALUES (%s, %s)
        """, (closet_id, outfit_id))
        db.get_db().commit()
        cursor.close()
        return jsonify({"message": "Outfit added to closet successfully", "storage_id": bridge_id}),201, 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customer.route("/customer/<int:customer_id>/wishlists", methods=["GET"])
def get_customer_wishlist(customer_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT cw.WishlistID, ci.Name, ci.Price, ci.ImageAddress
            FROM CustomerWishlist cw
            JOIN CustWishListClothingItem cwci ON cw.WishlistID = cwci.WishlistID
            JOIN ClothingItem ci ON cwci.ClothingItemID = ci.ItemID
            WHERE cw.CustomerID = %s
        """, (customer_id,))
        items = cursor.fetchall()
        cursor.execute("""
            SELECT DISTINCT ci.Name, ci.Price, a.Name AS SharedAesthetic
            FROM CustomerWishlist cw
            JOIN CustWishListClothingItem cwci ON cw.WishlistID = cwci.WishlistID
            JOIN ClothingItem ci ON cwci.ClothingItemID = ci.ItemID
            JOIN ClothingItemMatchedAesthetic cima_wish ON ci.ItemID = cima_wish.ClothingItemID
            JOIN Aesthetic a ON cima_wish.AestheticID = a.AestheticID
            WHERE cw.CustomerID = %s
            AND a.AestheticID IN (
                SELECT DISTINCT cima_closet.AestheticID
                FROM CustomerCloset cc
                JOIN CustomerClosetClothingItems cci ON cc.ClosetID = cci.ClosetID
                JOIN ClothingItemMatchedAesthetic cima_closet ON cci.ClothingItemID = cima_closet.ClothingItemID
                WHERE cc.CustomerID = %s
            )
        """, (customer_id, customer_id))
        matches = cursor.fetchall()

        cursor.close()
        return jsonify({"wishlist": items, "aesthetic_matches": matches}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customer.route("/customer/<int:customer_id>/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["POST"])
def add_customer_wishlist_item(customer_id, wishlist_id, item_id):
    try:
       cursor = db.get_db().cursor()
       cursor.execute("SELECT MAX(ItemId) FROM CustWishListClothingItem")
       res = cursor.fetchone()
       bridge_id = (res['MAX(ItemId)'] or 400) + 1
       cursor.execute("SELECT WishlistID FROM CustomerWishlist WHERE CustomerID = %s", (customer_id,))
       inv_row = cursor.fetchone()
       if not inv_row: 
            return jsonify({"error": "No closet found"}), 404     
       cursor.execute("""
            INSERT INTO CustWishListClothingItem (ItemID, WishlistID, ClothingItemID)
            VALUES (%s, %s, %s)
        """, (bridge_id, wishlist_id, item_id))
       db.get_db().commit()
       cursor.close()
       return jsonify({"message": "Item added to wishlist successfully", "storage_id": bridge_id}),201, 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    





