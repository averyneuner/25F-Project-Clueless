DROP DATABASE IF EXISTS Clueless;
CREATE DATABASE Clueless;
USE Clueless;

DROP TABLE IF EXISTS Customer;
CREATE TABLE IF NOT EXISTS Customer (
	CustomerID INT PRIMARY KEY,
    EmailAddress VARCHAR(50),
    FirstName VARCHAR(50),
	LastName VARCHAR(50),
    StreetAddress VARCHAR(100),
    City VARCHAR(50),
    State VARCHAR(50),
    ZIP VARCHAR(10),
    Country VARCHAR(50)
);

DROP TABLE IF EXISTS Business;
CREATE TABLE IF NOT EXISTS Business (
	CompanyID INT PRIMARY KEY,
	CompanyName VARCHAR(50),
	ContactEmail VARCHAR(50),
    StreetAddress VARCHAR(100),
    City VARCHAR(50),
    State VARCHAR(50),
    ZIP VARCHAR(10),
    Country VARCHAR(50),
    PopularityPercentage DECIMAL(4,2)
);

DROP TABLE IF EXISTS CustomerCloset;
CREATE TABLE IF NOT EXISTS CustomerCloset (
	ClosetID INT PRIMARY KEY,
	NickName VARCHAR(50),
	CustomerID INT,
	FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

DROP TABLE IF EXISTS CustomerWishlist;
CREATE TABLE IF NOT EXISTS CustomerWishlist (
	WishlistID INT PRIMARY KEY,
	Nickname VARCHAR(50),
    CustomerID INT,
	FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

DROP TABLE IF EXISTS CustomerNotification;
CREATE TABLE IF NOT EXISTS CustomerNotification (
	NotificationID INT PRIMARY KEY,
	Message VARCHAR(50),
	Status VARCHAR(50),
    CustomerID INT,
	FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

DROP TABLE IF EXISTS BusinessNotification;
CREATE TABLE IF NOT EXISTS BusinessNotification (
	NotificationID INT PRIMARY KEY,
	Message VARCHAR(50),
	Status VARCHAR(50),
    CompanyID INT,
	FOREIGN KEY (CompanyID) REFERENCES Business(CompanyID)
);

DROP TABLE IF EXISTS BusinessWishlist;
CREATE TABLE IF NOT EXISTS BusinessWishlist (
	WishlistID INT PRIMARY KEY,
	Nickname VARCHAR(50),
	CompanyID INT,
	FOREIGN KEY (CompanyID) REFERENCES Business(CompanyID)
);

DROP TABLE IF EXISTS BusinessInventory;
CREATE TABLE IF NOT EXISTS BusinessInventory (
	InventoryID INT PRIMARY KEY,
	Title VARCHAR(50),
	CompanyID INT,
	FOREIGN KEY (CompanyID) REFERENCES Business(CompanyID)
);

DROP TABLE IF EXISTS Outfit;
CREATE TABLE IF NOT EXISTS Outfit (
	OutfitID INT PRIMARY KEY,
	Nickname VARCHAR(50),
	Description TEXT
);

DROP TABLE IF EXISTS ClothingItem;
CREATE TABLE IF NOT EXISTS ClothingItem (
	ItemID INT PRIMARY KEY,
	ImageAddress VARCHAR(50),
	Name VARCHAR(50),
	Category VARCHAR(50),
	Price DECIMAL(4,2),
	Size VARCHAR(50),
	QualityRating INT,
    OutdatedFlag BOOLEAN,
PopularityPercentage DECIMAL(4,2)
);

DROP TABLE IF EXISTS Aesthetic;
CREATE TABLE IF NOT EXISTS Aesthetic (
	AestheticID INT PRIMARY KEY,
	Name VARCHAR(50),
	Description TEXT,
	PopularityPercent DECIMAL(4,2)
);

DROP TABLE IF EXISTS `System`;
CREATE TABLE `System` (
   SystemID INT PRIMARY KEY,
   UserName VARCHAR(50),
   Password VARCHAR(50),
   IssueLogs VARCHAR(255),
   BusinessNotifID INT,
   CustomerNotifID INT,
   FOREIGN KEY (BusinessNotifID) REFERENCES BusinessNotification(NotificationID),
   FOREIGN KEY (CustomerNotifID) REFERENCES CustomerNotification(NotificationID)
);


DROP TABLE IF EXISTS TechTeam;
CREATE TABLE TechTeam (
   TechID INT PRIMARY KEY,
   Name VARCHAR(50),
   Department VARCHAR(50),
   SystemID INT,
   FOREIGN KEY (SystemID) REFERENCES `System`(SystemID)
);

DROP TABLE IF EXISTS OutfitMatchedAesthetic;
CREATE TABLE OutfitMatchedAesthetic (
	AestheticID INT,
	OutfitID INT,
	PRIMARY KEY (AestheticID, OutfitID),
	FOREIGN KEY (AestheticID) REFERENCES Aesthetic(AestheticID),
	FOREIGN KEY (OutfitID) REFERENCES Outfit(OutfitID)
);

DROP TABLE IF EXISTS ClothingItemMatchedAesthetic;
CREATE TABLE ClothingItemMatchedAesthetic (
	AestheticID INT,
	ClothingItemID INT,
	PRIMARY KEY (AestheticID, ClothingItemID),
	FOREIGN KEY (AestheticID) REFERENCES Aesthetic(AestheticID),
	FOREIGN KEY (ClothingItemID) REFERENCES ClothingItem(ItemID)
);

DROP TABLE IF EXISTS CustomerOutfitsOfClothingItems;
CREATE TABLE CustomerOutfitsOfClothingItems (
	ClothingItemID INT,
	OutfitID INT,
	PRIMARY KEY (ClothingItemID, OutfitID),
	FOREIGN KEY (ClothingItemID) REFERENCES ClothingItem(ItemID),
	FOREIGN KEY (OutfitID) REFERENCES Outfit(OutfitID)
);

DROP TABLE IF EXISTS CustomerClosetOutfits;
CREATE TABLE CustomerClosetOutfits (
	ClosetID INT,
	OutfitID INT,
	PRIMARY KEY (ClosetID, OutfitID),
	FOREIGN KEY (ClosetID) REFERENCES CustomerCloset(ClosetID),
	FOREIGN KEY (OutfitID) REFERENCES Outfit(OutfitID)
);

DROP TABLE IF EXISTS CustomerClosetClothingItems;
CREATE TABLE CustomerClosetClothingItems (
	ClothingItemID INT,
	ClosetID INT,
    NumberofWears INT,
    AvailabilityStatus BOOLEAN,
	PRIMARY KEY (ClothingItemID, ClosetID),
	FOREIGN KEY (ClothingItemID) REFERENCES ClothingItem(ItemID),
	FOREIGN KEY (ClosetID) REFERENCES CustomerCloset(ClosetID)
);

DROP TABLE IF EXISTS CustWishListClothingItem;
CREATE TABLE CustWishListClothingItem (
	ItemID INT,
	WishlistID INT,
    ClothingItemID INT,
	PRIMARY KEY (ItemId, WishlistID),
	FOREIGN KEY (ClothingItemID) REFERENCES ClothingItem(ItemID),
    FOREIGN KEY (WishlistID) REFERENCES CustomerWishlist(WishlistID)
);

DROP TABLE IF EXISTS BusinessWishlistClothingItem;
CREATE TABLE BusinessWishlistClothingItem (
	ItemID INT,
	WishlistID INT,
    ClothingItemID INT,
	PRIMARY KEY (ItemId, WishlistID),
	FOREIGN KEY (ClothingItemID) REFERENCES ClothingItem(ItemID),
    FOREIGN KEY (WishlistID) REFERENCES BusinessWishlist(WishlistID)
);

DROP TABLE IF EXISTS BusinessInventoryItemStorage;
CREATE TABLE BusinessInventoryItemStorage (
	ItemID INT,
	InventoryID INT,
	EthicallySourcedFlag BOOLEAN,
	UnitsSold INT,
	QuantityInStock INT,
    ClothingItemID INT,
	PRIMARY KEY (ItemId, InventoryID),
	FOREIGN KEY (ClothingItemID) REFERENCES ClothingItem(ItemID),
FOREIGN KEY (InventoryID) REFERENCES BusinessInventory(InventoryID)
);

INSERT INTO Customer (CustomerID, EmailAddress, FirstName, LastName, StreetAddress, City, State, ZIP, Country) VALUES
(1, 'emma@example.com', 'Emma', 'Chen',
'12 Garden Ave', 'Boston', 'MA', '02115', 'USA'),
(2, 'liam@example.com', 'Liam', 'Diaz',
'90 River St', 'Cambridge', 'MA', '02139', 'USA'),
(3, 'sophia@example.com', 'Sophia', 'Patel',
'44 Beacon Rd', 'Somerville', 'MA', '02143', 'USA');


INSERT INTO Business (CompanyID, CompanyName, ContactEmail, StreetAddress, City, State, ZIP, Country, PopularityPercentage) VALUES
(1, 'Urban Outfitters', 'contact@urbanoutfitters.com', '10 Market St',
'Boston', 'MA', '02120', 'USA', 75.50),
(2, 'EcoWear', 'support@ecowear.com', '5 Green Lane',
'Cambridge', 'MA', '12412', 'USA', 62.30),
(3, 'FashionNova', 'hello@novafashion.com', '200 Blank Blvd',
'Somerville', 'MA', '12342', 'USA', 88.10);

INSERT INTO CustomerCloset (ClosetID, NickName, CustomerID)
VALUES
(101, 'Everyday', 1),
(102, 'Work', 2),
(103, 'Night Out', 3);

INSERT INTO CustomerWishlist (WishlistID, Nickname, CustomerID)
VALUES
(201, 'Fall Wishlist', 1),
(202, 'School Wishlist', 2),
(203, 'Christmas Wishlist', 3);

INSERT INTO CustomerNotification (NotificationID, Message, Status, CustomerID)
VALUES
(301, 'Your order has shipped', 'Unread', 1),
(302, 'New items match your aesthetic', 'Unread', 2),
(303, 'Price drop on items in your wishlist', 'Read', 3);

INSERT INTO BusinessNotification (NotificationID, Message, Status, CompanyID)
VALUES
(401, 'Is demand for hoodies in Medium still high?', 'Sent', 1),
(402, 'High demand for baggy jeans this week', 'Sent', 2),
(403, 'Are users engaging with minimalist accessories?', 'Sent', 3);

INSERT INTO BusinessWishlist (WishlistID, Nickname, CompanyID)
VALUES
(501, 'High Demand Skirt', 1),
(502, 'Shoes On Trend', 2),
(503, 'High-Traffic Items', 3);

INSERT INTO BusinessInventory (InventoryID, Title, CompanyID)
VALUES
(601, 'Winter Lineup', 1),
(602, 'Eco Collection', 2),
(603, 'Streetwear Drop', 3);

INSERT INTO Outfit (OutfitID, Nickname, Description)
VALUES
(701, 'Cozy Fall Fit', 'Sweater + jeans + boots'),
(702, 'Gym Essentials', 'Leggings + tank + sneakers'),
(703, 'Night Out', 'Black dress + heels');

INSERT INTO ClothingItem (ItemID, ImageAddress, Name, Category, Price, Size, QualityRating, PopularityPercentage)
VALUES
(801, 'img/hoodie1.jpg', 'Cute Hoodie', 'Hoodie', 49.99, 'M',
8, 72.10),
(802, 'img/jeans1.jpg', 'Baggy Jeans', 'Pants', 59.99, 'L',
7, 84.30),
(803, 'img/dress1.jpg', 'Black Evening Dress', 'Dress', 79.50, 'S',
9, 90.00);

INSERT INTO Aesthetic (AestheticID, Name, Description, PopularityPercent)
VALUES
(901, 'Minimalist', 'Neutral colors', 65.20),
(902, 'Streetwear', 'Baggy, bold', 82.40),
(903, 'Elegant', 'Refined, evening wear vibes', 74.80);

INSERT INTO `System` (SystemID, UserName, Password, IssueLogs, BusinessNotifID, CustomerNotifID)
VALUES
(1001, 'sysadmin1', 'pass123', 'No issues reported', 401,
301),
(1002, 'sysadmin2', '123', 'Minor lag in database sync', 402,
302),
(1003, 'sysadmin3', 'pass', 'Intermittent API timeout errors',
403, 303);

INSERT INTO TechTeam (TechID, Name, Department, SystemID)
VALUES
(2001, 'Jenna Kim', 'Backend', 1001),
(2002, 'Bella Lopez', 'Infrastructure', 1002),
(2003, 'Priya Basker', 'Security', 1003);

INSERT INTO OutfitMatchedAesthetic (AestheticID, OutfitID)
VALUES
(901, 701),
(902, 702),
(903, 703),
(901, 702);;

INSERT INTO ClothingItemMatchedAesthetic (AestheticID, ClothingItemID)
VALUES
(901, 801),
(902, 802),
(903, 803);

INSERT INTO CustomerOutfitsOfClothingItems (ClothingItemID, OutfitID)
VALUES
(801, 701),
(802, 702),
(803, 703);

INSERT INTO CustomerClosetOutfits (ClosetID, OutfitID)
VALUES
(101, 701),
(102, 702),
(103, 703);

INSERT INTO CustomerClosetClothingItems (ClothingItemID, ClosetID, NumberofWears, AvailabilityStatus)
VALUES
(801, 101, 7, TRUE),
(802, 102, 3, TRUE),
(803, 103, 4, TRUE);

INSERT INTO CustWishListClothingItem (ItemID, WishlistID, ClothingItemID)
VALUES
(801, 201, 801),
(802, 202, 802),
(803, 203, 803);

INSERT INTO BusinessWishlistClothingItem (ItemID, WishlistID, ClothingItemID)
VALUES
(801, 501, 801),
(802, 502, 802),
(803, 503, 803);

INSERT INTO BusinessInventoryItemStorage (ItemID, InventoryID, EthicallySourcedFlag, UnitsSold, QuantityInStock, ClothingItemID)
VALUES
(801, 601, TRUE, 120, 40, 801),
(802, 602, FALSE, 95, 55, 802),
(803, 603, TRUE, 60, 20, 803);
