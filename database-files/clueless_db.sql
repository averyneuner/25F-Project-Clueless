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
	Price DECIMAL(7,2),
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
(10, 'olivia.r@example.com', 'Olivia', 'Rodriguez', '12 Sunset Blvd', 'Los Angeles', 'CA', '90001', 'USA'),
(11, 'jackson.t@example.com', 'Jackson', 'Thompson', '88 Highland Park', 'Austin', 'TX', '78701', 'USA'),
(12, 'sophie.l@example.com', 'Sophie', 'Lee', '452 Broadway', 'New York', 'NY', '10012', 'USA'),
(13, 'rachel.green@example.com', 'Rachel', 'Green', '18 West 11th Street', 'New York', 'NY', '10011', 'USA'),
(14, 'isabella.m@example.com', 'Isabella', 'Martinez', '303 Peachtree St', 'Atlanta', 'GA', '30303', 'USA'),
(15, 'mason.g@example.com', 'Mason', 'Garcia', '500 Brickell Ave', 'Miami', 'FL', '33131', 'USA'),
(16, 'charlotte.w@example.com', 'Charlotte', 'Wilson', '77 Newbury St', 'Boston', 'MA', '02116', 'USA'),
(17, 'elijah.b@example.com', 'Elijah', 'Brooks', '1200 Market St', 'Philadelphia', 'PA', '19107', 'USA'),
(18, 'amelia.h@example.com', 'Amelia', 'Hall', '555 Pike St', 'Seattle', 'WA', '98101', 'USA'),
(19, 'lucas.y@example.com', 'Lucas', 'Young', '101 California St', 'San Francisco', 'CA', '94111', 'USA'),
(20, 'harper.a@example.com', 'Harper', 'Allen', '200 Main St', 'Dallas', 'TX', '75201', 'USA'),
(21, 'ben.king@example.com', 'Benjamin', 'King', '404 Capitol Way', 'Olympia', 'WA', '98501', 'USA'),
(22, 'evelyn.s@example.com', 'Evelyn', 'Scott', '789 State St', 'Madison', 'WI', '53703', 'USA'),
(23, 'alex.green@example.com', 'Alexander', 'Green', '321 Bourbon St', 'New Orleans', 'LA', '70130', 'USA'),
(24, 'mia.baker@example.com', 'Mia', 'Baker', '654 Hennepin Ave', 'Minneapolis', 'MN', '55403', 'USA'),
(25, 'james.hill@example.com', 'James', 'Hill', '987 Broadway', 'Nashville', 'TN', '37203', 'USA'),
(26, 'ava.carter@example.com', 'Ava', 'Carter', '147 Las Vegas Blvd', 'Las Vegas', 'NV', '89109', 'USA'),
(27, 'henry.p@example.com', 'Henry', 'Phillips', '258 Congress St', 'Portland', 'ME', '04101', 'USA'),
(28, 'ella.m@example.com', 'Ella', 'Mitchell', '369 Santa Fe Dr', 'Denver', 'CO', '80204', 'USA'),
(29, 'sam.campbell@example.com', 'Samuel', 'Campbell', '159 Camelback Rd', 'Phoenix', 'AZ', '85016', 'USA'),
(30, 'luna.rivera@example.com', 'Luna', 'Rivera', '753 Wynwood Walls', 'Miami', 'FL', '33127', 'USA'),
(31, 'david.cooper@example.com', 'David', 'Cooper', '951 Pearl St', 'Boulder', 'CO', '80302', 'USA'),
(32, 'victoria.ward@example.com', 'Victoria', 'Ward', '357 King St', 'Charleston', 'SC', '29401', 'USA'),
(33, 'joseph.turner@example.com', 'Joseph', 'Turner', '123 Beale St', 'Memphis', 'TN', '38103', 'USA'),
(34, 'grace.parker@example.com', 'Grace', 'Parker', '456 Sundance Sq', 'Fort Worth', 'TX', '76102', 'USA'),
(35, 'daniel.evans@example.com', 'Daniel', 'Evans', '789 Fourth St', 'Louisville', 'KY', '40202', 'USA'),
(36, 'chloe.collins@example.com', 'Chloe', 'Collins', '321 River St', 'Savannah', 'GA', '31401', 'USA'),
(37, 'matthew.stewart@example.com', 'Matthew', 'Stewart', '654 High St', 'Columbus', 'OH', '43215', 'USA'),
(38, 'zoe.sanchez@example.com', 'Zoe', 'Sanchez', '987 Old Town', 'San Diego', 'CA', '92110', 'USA'),
(39, 'jack.morris@example.com', 'Jack', 'Morris', '147 Hawthorne Blvd', 'Portland', 'OR', '97214', 'USA'),
(40, 'penelope.rogers@example.com', 'Penelope', 'Rogers', '258 Temple Sq', 'Salt Lake City', 'UT', '84150', 'USA'),
(41, 'levi.reed@example.com', 'Levi', 'Reed', '369 Monument Cir', 'Indianapolis', 'IN', '46204', 'USA'),
(42, 'mila.cook@example.com', 'Mila', 'Cook', '159 Elmwood Ave', 'Buffalo', 'NY', '14222', 'USA'),
(43, 'owen.morgan@example.com', 'Owen', 'Morgan', '753 Woodward Ave', 'Detroit', 'MI', '48201', 'USA'),
(44, 'layla.bell@example.com', 'Layla', 'Bell', '951 Falls St', 'Raleigh', 'NC', '27601', 'USA'),
(45, 'wyatt.murphy@example.com', 'Wyatt', 'Murphy', '357 Brady St', 'Tulsa', 'OK', '74103', 'USA');

INSERT INTO Business (CompanyID, CompanyName, ContactEmail, StreetAddress, City, State, ZIP, Country, PopularityPercentage) VALUES
(10, 'Gucci', 'contact@gucci.com', '195 Broadway', 'New York', 'NY', '10007', 'USA', 94.50),
(11, 'Gap', 'support@gap.com', '2 Folsom St', 'San Francisco', 'CA', '94105', 'USA', 76.20),
(12, 'Target Style', 'fashion@target.com', '1000 Nicollet Mall', 'Minneapolis', 'MN', '55403', 'USA', 88.90),
(13, 'Anthropologie', 'hello@anthropologie.com', '50 South 16th St', 'Philadelphia', 'PA', '19102', 'USA', 82.10),
(14, 'Supreme', 'info@supremenewyork.com', '274 Lafayette St', 'New York', 'NY', '10012', 'USA', 91.00),
(15, 'Lululemon', 'guest.services@lululemon.com', '1818 Cornwall Ave', 'Vancouver', 'BC', 'V6J1C7', 'Canada', 89.50),
(16, 'Madewell', 'help@madewell.com', '770 Broadway', 'New York', 'NY', '10003', 'USA', 79.40),
(17, 'Nike', 'media.relations@nike.com', '1 Bowerman Dr', 'Beaverton', 'OR', '97005', 'USA', 96.20),
(18, 'Adidas', 'service@adidas.com', '5055 N Greeley Ave', 'Portland', 'OR', '97217', 'USA', 93.80),
(19, 'Reformation', 'love@thereformation.com', '2263 E Vernon Ave', 'Vernon', 'CA', '90058', 'USA', 84.60),
(20, 'Everlane', 'support@everlane.com', '2170 Folsom St', 'San Francisco', 'CA', '94110', 'USA', 77.30),
(21, 'Aritzia', 'concierge@aritzia.com', '611 Alexander St', 'Vancouver', 'BC', 'V6A1E1', 'Canada', 81.50),
(22, 'Free People', 'service@freepeople.com', '5000 S Broad St', 'Philadelphia', 'PA', '19112', 'USA', 78.90),
(23, 'Nordstrom', 'contact@nordstrom.com', '1617 6th Ave', 'Seattle', 'WA', '98101', 'USA', 86.40),
(24, 'Levi Strauss', 'help@levi.com', '1155 Battery St', 'San Francisco', 'CA', '94111', 'USA', 90.10),
(25, 'Ralph Lauren', 'customer.service@ralphlauren.com', '650 Madison Ave', 'New York', 'NY', '10022', 'USA', 87.50),
(26, 'Calvin Klein', 'service@calvinklein.com', '205 W 39th St', 'New York', 'NY', '10018', 'USA', 85.30),
(27, 'Tommy Hilfiger', 'help@tommy.com', '285 Madison Ave', 'New York', 'NY', '10017', 'USA', 83.70),
(28, 'Chanel', 'clientservice@chanel.com', '9 W 57th St', 'New York', 'NY', '10019', 'USA', 95.80),
(29, 'Prada', 'client.service.americas@prada.com', '611 5th Ave', 'New York', 'NY', '10022', 'USA', 94.20),
(30, 'Louis Vuitton', 'us.service@louisvuitton.com', '1 E 57th St', 'New York', 'NY', '10022', 'USA', 95.50),
(31, 'Burberry', 'us.customerservice@burberry.com', '444 Madison Ave', 'New York', 'NY', '10022', 'USA', 92.60),
(32, 'Dior', 'contactdior@dior.com', '131 Spring St', 'New York', 'NY', '10012', 'USA', 94.80),
(33, 'Versace', 'customer.care@versace.com', '645 5th Ave', 'New York', 'NY', '10022', 'USA', 93.10),
(34, 'Balenciaga', 'clientservice.us@balenciaga.com', '840 Madison Ave', 'New York', 'NY', '10021', 'USA', 91.50),
(35, 'Saint Laurent', 'clientservice@ysl.com', '3 E 57th St', 'New York', 'NY', '10022', 'USA', 92.90),
(36, 'Fendi', 'client.services.us@fendi.com', '598 Madison Ave', 'New York', 'NY', '10022', 'USA', 91.80),
(37, 'Givenchy', 'contact@givenchy.com', '747 Madison Ave', 'New York', 'NY', '10065', 'USA', 90.50),
(38, 'Valentino', 'customercare@valentino.com', '693 5th Ave', 'New York', 'NY', '10022', 'USA', 92.20),
(39, 'Hermes', 'service.us@hermes.com', '691 Madison Ave', 'New York', 'NY', '10065', 'USA', 96.50),
(40, 'Rebecca Boutique', 'rebecca.us@boutique.com', '809 Eleven Levels', 'New Haven', 'CT', '99882', 'USA', 88.7);

INSERT INTO ClothingItem (ItemID, ImageAddress, Name, Category, Price, Size, QualityRating, OutdatedFlag, PopularityPercentage) VALUES
(820, 'img/silkscarf.jpg', 'Vintage Silk Scarf', 'Accessory', 120.00, 'OneSize', 9, FALSE, 78.00),
(821, 'img/leatherskirt.jpg', 'Faux Leather Skirt', 'Skirt', 45.00, 'S', 7, FALSE, 85.00),
(822, 'img/bomber.jpg', 'Olive Bomber Jacket', 'Jacket', 89.99, 'L', 8, FALSE, 82.00),
(823, 'img/turtleneck.jpg', 'Black Turtleneck', 'Top', 29.99, 'M', 8, FALSE, 75.00),
(824, 'img/wideleg.jpg', 'Wide Leg Linen Pants', 'Pants', 60.00, 'S', 9, FALSE, 88.00),
(825, 'img/denimjacket.jpg', 'Oversized Denim Jacket', 'Jacket', 75.00, 'XL', 10, FALSE, 91.00),
(826, 'img/slipdress.jpg', 'Satin Slip Dress', 'Dress', 55.00, 'M', 7, FALSE, 80.00),
(827, 'img/corset.jpg', 'Lace Corset Top', 'Top', 40.00, 'S', 6, FALSE, 92.00),
(828, 'img/blazer.jpg', 'Plaid Oversized Blazer', 'Jacket', 95.00, 'L', 8, TRUE, 70.00),
(829, 'img/miniskirt.jpg', 'Pleated Tennis Skirt', 'Skirt', 35.00, 'XS', 7, FALSE, 89.00),
(830, 'img/docmartens.jpg', 'Combat Boots', 'Shoes', 160.00, '8', 10, FALSE, 94.00),
(831, 'img/converse.jpg', 'High Top Sneakers', 'Shoes', 65.00, '9', 8, FALSE, 90.00),
(832, 'img/beanie.jpg', 'Fisherman Beanie', 'Accessory', 20.00, 'OneSize', 9, FALSE, 83.00),
(833, 'img/trench.jpg', 'Classic Trench Coat', 'Jacket', 180.00, 'M', 9, FALSE, 76.00),
(834, 'img/bucket.jpg', 'Fuzzy Bucket Hat', 'Accessory', 25.00, 'OneSize', 6, TRUE, 87.00),
(835, 'img/vest.jpg', 'Puffer Vest', 'Jacket', 50.00, 'L', 8, FALSE, 72.00),
(836, 'img/cardigan.jpg', 'Chunky Knit Cardigan', 'Top', 60.00, 'M', 9, FALSE, 81.00),
(837, 'img/leggings.jpg', 'High Waisted Leggings', 'Pants', 90.00, 'S', 10, FALSE, 95.00),
(838, 'img/flannel.jpg', 'Vintage Flannel Shirt', 'Top', 30.00, 'XL', 7, FALSE, 79.00),
(839, 'img/maxi.jpg', 'Boho Maxi Skirt', 'Skirt', 45.00, 'L', 8, FALSE, 74.00),
(840, 'img/croptop.jpg', 'White Ribbed Crop', 'Top', 15.00, 'S', 6, FALSE, 93.00),
(841, 'img/shorts.jpg', 'Distressed Denim Shorts', 'Pants', 40.00, 'M', 7, FALSE, 86.00),
(842, 'img/tracksuit.jpg', 'Velour Tracksuit', 'Set', 80.00, 'L', 5, TRUE, 65.00),
(843, 'img/boots2.jpg', 'Knee High Boots', 'Shoes', 120.00, '7', 8, FALSE, 84.00),
(844, 'img/bag.jpg', 'Baguette Bag', 'Accessory', 200.00, 'OneSize', 9, FALSE, 88.00),
(845, 'img/sunglasses.jpg', 'Cat Eye Sunglasses', 'Accessory', 150.00, 'OneSize', 9, FALSE, 82.00),
(846, 'img/polo.jpg', 'Striped Polo Shirt', 'Top', 55.00, 'L', 8, FALSE, 70.00),
(847, 'img/khakis.jpg', 'Pleated Khakis', 'Pants', 60.00, '34', 8, TRUE, 60.00),
(848, 'img/fedora.jpg', 'Wool Fedora', 'Accessory', 45.00, 'M', 7, TRUE, 55.00),
(849, 'img/sandals.jpg', 'Leather Slides', 'Shoes', 80.00, '10', 9, FALSE, 85.00),
(850, 'img/pajamas.jpg', 'Silk Pajama Set', 'Set', 110.00, 'M', 10, FALSE, 77.00),
(851, 'img/gloves.jpg', 'Cashmere Gloves', 'Accessory', 60.00, 'M', 9, FALSE, 80.00),
(852, 'img/belt.jpg', 'Logo Belt', 'Accessory', 350.00, 'M', 10, FALSE, 89.00),
(853, 'img/watch.jpg', 'Gold Digital Watch', 'Accessory', 75.00, 'OneSize', 8, TRUE, 73.00),
(854, 'img/socks.jpg', 'Tube Socks', 'Accessory', 10.00, 'L', 6, FALSE, 81.00);

INSERT INTO Aesthetic (AestheticID, Name, Description, PopularityPercent) VALUES
(908, 'Dark Academia', 'Tweeds, books, earthy tones', 88.00),
(909, 'Cyberpunk', 'Neon, tech-wear, futuristic', 65.00),
(910, 'Boho Chic', 'Flowy, patterns, natural fabrics', 72.00),
(911, 'Grunge', 'Flannels, distressed, dark colors', 79.00),
(912, 'Old Money', 'Quiet luxury, polos, tennis whites', 85.00),
(913, 'Soft Girl', 'Pastels, clips, cute motifs', 81.00),
(914, 'Normcore', 'Unpretentious, average, plain clothing', 55.00),
(915, 'Biker', 'Leather jackets, boots, black denim', 76.00),
(916, 'Athleisure', 'Gym wear as daily wear', 95.00),
(917, 'Kawaii', 'Cute, pink, frills', 70.00);

INSERT INTO CustomerCloset (ClosetID, NickName, CustomerID) VALUES
(109, 'Gym Bag', 10), (110, 'Office Fits', 10),
(111, 'Date Night', 11), (112, 'Casual', 11),
(113, 'Summer 2025', 12), (114, 'Winter Vault', 12),
(115, 'Interview Clothes', 13), (116, 'Lounge', 13),
(117, 'Party Wear', 14), (118, 'Beach Trip', 14),
(119, 'Hiking', 15), (120, 'Daily Rotation', 15),
(121, 'Formal Events', 16), (122, 'Work From Home', 16),
(123, 'Festival Gear', 17), (124, 'Cozy', 17),
(125, 'Travel', 18), (126, 'Basics', 18),
(127, 'Statement Pieces', 19), (128, 'Shoes Only', 19),
(129, 'Accessories', 20), (130, 'Vintage Finds', 20),
(131, 'Capsule Wardrobe', 21), (132, 'Rainy Day', 21),
(133, 'Clubbing', 22), (134, 'Brunch', 22),
(135, 'Uni Outfits', 23), (136, 'Exam Week', 23),
(137, 'Spring Cleaning', 24), (138, 'Donate Pile', 24),
(139, 'Borrowed', 25), (140, 'Costumes', 25),
(141, 'Ski Trip', 26), (142, 'Poolside', 26),
(143, 'Layering', 27), (144, 'Outerwear', 27),
(145, 'Denim Collection', 28), (146, 'Activewear', 28),
(147, 'Sleepwear', 29), (148, 'Date Night', 29),
(149, 'Work Uniform', 30), (150, 'Weekend', 30),
(151, 'Running', 31), (152, 'Camping', 31),
(153, 'Wedding Guest', 32), (154, 'Cocktail', 32),
(155, 'Business Trip', 33), (156, 'Casual Friday', 33),
(157, 'Concert', 34), (158, 'Rodeo', 34),
(159, 'Derby Day', 35), (160, 'Golf', 35),
(161, 'Tea Party', 36), (162, 'Garden', 36),
(163, 'Tailgate', 37), (164, 'Gameday', 37),
(165, 'Surfing', 38), (166, 'Skating', 38),
(167, 'Hipster', 39), (168, 'Coffee Shop', 39),
(169, 'Sunday Best', 40), (170, 'Choir', 40);

INSERT INTO CustomerWishlist (WishlistID, Nickname, CustomerID) VALUES
(209, 'Birthday Gifts', 10), (210, 'Black Friday', 11),
(211, 'Dream Bag', 12), (212, 'Next Paycheck', 13),
(213, 'Wedding Season', 14), (214, 'Europe Trip', 15),
(215, 'New Job', 16), (216, 'Winter Coat', 17),
(217, 'Sneakerhead', 18), (218, 'Techwear', 19),
(219, 'Jewelry', 20), (220, 'Watches', 21),
(221, 'Sales Only', 22), (222, 'Luxury', 23),
(223, 'Must Haves', 24), (224, 'Maybe', 25),
(225, 'Influencer Picks', 26), (226, 'As Seen On TV', 27),
(227, 'Camping Gear', 28), (228, 'Yoga', 29),
(229, 'Swim', 30), (230, 'Climbing', 31),
(231, 'Formal', 32), (232, 'Suits', 33),
(233, 'Boots', 34), (234, 'Hats', 35),
(235, 'Scarves', 36), (236, 'Gloves', 37),
(237, 'Sunglasses', 38), (238, 'Belts', 39),
(239, 'Ties', 40), (240, 'Socks', 41),
(241, 'Underwear', 42), (242, 'Pajamas', 43),
(243, 'Robes', 44), (244, 'Slippers', 45),
(245, 'Cyber Monday', 10), (246, 'Christmas', 11),
(247, 'Hanukkah', 12), (248, 'Valentine', 13),
(249, 'Easter', 14), (250, 'Halloween', 15),
(251, 'Thanksgiving', 16), (252, 'New Year', 17),
(253, 'Graduation', 18), (254, 'Anniversary', 19),
(255, 'Baby Shower', 20), (256, 'Bridal Shower', 21),
(257, 'Housewarming', 22), (258, 'Retirement', 23),
(259, 'Just Because', 24), (260, 'Treat Yourself', 25),
(261, 'Splurge', 26), (262, 'Save For Later', 27),
(263, 'Out of Stock', 28), (264, 'Pre-order', 29),
(265, 'Back to School', 30), (266, 'Spring Break', 31),
(267, 'Summer Vacation', 32), (268, 'Winter Break', 33);

INSERT INTO BusinessWishlist (WishlistID, Nickname, CompanyID) VALUES
(507, 'Sustainable Fabrics', 10), (508, 'Recycled Denim', 11),
(509, 'Organic Cotton', 12), (510, 'Vegan Leather', 13),
(511, 'Hemp Blends', 14), (512, 'Bamboo Fiber', 15),
(513, 'Tencel', 16), (514, 'Smart Fabrics', 17),
(515, '3D Printed Soles', 18), (516, 'Deadstock', 19),
(517, 'Carbon Neutral', 20), (518, 'Fair Trade', 21),
(519, 'Local Wool', 22), (520, 'Handmade', 23),
(521, 'Upcycled', 24), (522, 'Vintage Wash', 25),
(523, 'Performance Mesh', 26), (524, 'Waterproof', 27),
(525, 'Windbreaker', 28), (526, 'Reflective', 29),
(527, 'Glow in Dark', 30), (528, 'Holographic', 31),
(529, 'Metallic', 32), (530, 'Neoprene', 33),
(531, 'Velvet', 34), (532, 'Corduroy', 35),
(533, 'Sequin', 36), (534, 'Embroidery', 37),
(535, 'Patchwork', 38), (536, 'Tie Dye', 39),
(537, 'Acid Wash', 10), (538, 'Stone Wash', 11),
(539, 'Raw Denim', 12), (540, 'Selvedge', 13),
(541, 'Distressed', 14), (542, 'Ripped', 15),
(543, 'Frayed', 16), (544, 'Bleached', 17),
(545, 'Overdyed', 18), (546, 'Pigment Dyed', 19),
(547, 'Garment Dyed', 20), (548, 'Yarn Dyed', 21),
(549, 'Printed', 22), (550, 'Embossed', 23),
(551, 'Laser Cut', 24), (552, 'Knitted', 25),
(553, 'Crocheted', 26), (554, 'Woven', 27),
(555, 'Braided', 28), (556, 'Tufted', 29),
(557, 'Clothes', 28), (558, 'Cute', 40);

INSERT INTO BusinessInventory (InventoryID, Title, CompanyID) VALUES
(607, 'Spring 2025', 10), (608, 'Summer 2025', 11),
(609, 'Fall 2025', 12), (610, 'Winter 2025', 13),
(611, 'Resort 2025', 14), (612, 'Pre-Fall 2025', 15),
(613, 'Capsule 1', 16), (614, 'Capsule 2', 17),
(615, 'Collab X', 18), (616, 'Collab Y', 19),
(617, 'Limited Edition', 20), (618, 'Exclusive', 21),
(619, 'Outlet', 22), (620, 'Clearance', 23),
(621, 'New Arrivals', 24), (622, 'Best Sellers', 25),
(623, 'Trending', 26), (624, 'Basics', 27),
(625, 'Denim Lab', 28), (626, 'Outerwear', 29),
(627, 'Swim Shop', 30), (628, 'Active Shop', 31),
(629, 'Work Shop', 32), (630, 'Party Shop', 33),
(631, 'Wedding Shop', 34), (632, 'Gift Shop', 35),
(633, 'Baby Shop', 36), (634, 'Kids Shop', 37),
(635, 'Home Shop', 38), (636, 'Beauty Shop', 39),
(637, 'Accessories', 10), (638, 'Shoes', 11),
(639, 'Bags', 12), (640, 'Jewelry', 13),
(641, 'Watches', 14), (642, 'Eyewear', 15),
(643, 'Fragrance', 16), (644, 'Tech', 17),
(645, 'Stationery', 18), (646, 'Books', 19),
(647, 'Music', 20), (648, 'Art', 21),
(649, 'Decor', 22), (650, 'Kitchen', 23),
(651, 'Bath', 24), (652, 'Bedding', 25),
(653, 'Lighting', 26), (654, 'Rugs', 27),
(711, 'Clothes', 28), (656, 'Clothes', 40),
(655, 'Furniture', 28), (657, 'Garden', 29);

USE Clueless;

-- Adding Outfits to the table that will work with the CustomerOutfitsOfClothingItems
INSERT INTO Outfit (OutfitID, Nickname, Description) VALUES
(701, 'Streetwear', 'Layered streetwear outfit with bomber jacket and combat boots'),
(702, 'Running', 'Leggings, crop top, and sneakers for gym or errands'),
(703, 'Night Out', 'Corset top with mini skirt and knee-high boots'),
(704, 'Office Attire', 'Blazer, tailored pants, and structured bag'),
(705, 'Festival Attire', 'Maxi skirt, crop top, and layered accessories'),
(706, '2000s', 'Flannel shirt, distressed jeans, and boots'),
(707, 'Winter Clothes', 'Chunky knit sweater, trench coat, scarf, and gloves'),
(708, 'Costume Party', 'Velour tracksuit, platform shoes, and baguette bag');

-- Bridge: CustomerOutfitsOfClothingItems
-- Linking the new items (820+) to new outfits or existing ones. 
-- Creating a massive mix to hit >125 rows.
INSERT INTO CustomerOutfitsOfClothingItems (ClothingItemID, OutfitID) VALUES
(820, 701), (820, 703), (821, 703), (821, 708), (822, 702),
(822, 706), (823, 701), (823, 704), (824, 705), (824, 704),
(825, 702), (825, 706), (825, 708), (826, 703), (826, 705),
(827, 703), (827, 708), (828, 704), (828, 706), (829, 702),
(829, 708), (830, 706), (830, 707), (830, 708), (831, 702),
(831, 706), (832, 701), (832, 706), (832, 707), (833, 701),
(833, 704), (834, 702), (834, 705), (834, 708), (835, 701),
(835, 702), (835, 707), (836, 701), (836, 704), (836, 705),
(837, 702), (837, 707), (838, 701), (838, 706), (838, 707),
(839, 705), (839, 708), (840, 702), (840, 705), (840, 708),
(841, 702), (841, 705), (842, 702), (842, 706), (842, 708),
(843, 701), (843, 703), (843, 704), (844, 703), (844, 704),
(844, 708), (845, 702), (845, 705), (846, 704), (846, 707),
(847, 704), (848, 701), (848, 704), (849, 702), (849, 705),
(850, 701), (851, 701), (851, 707), (852, 703), (852, 704),
(853, 702), (853, 706), (854, 702), (854, 706), (854, 707),
(820, 705), (821, 706), (822, 708), (823, 703), (824, 701),
(825, 704), (826, 708), (827, 706), (828, 701), (829, 705),
(830, 702), (831, 708), (832, 705), (833, 703), (834, 706),
(835, 704), (836, 708), (837, 701), (838, 705), (839, 702),
(840, 706), (841, 708), (842, 703), (843, 705), (844, 701),
(845, 708), (846, 702), (847, 706), (848, 703), (849, 708),
(850, 705), (851, 704), (852, 706), (853, 708), (854, 701),
(820, 706), (821, 701), (822, 705), (823, 708), (824, 703),
(825, 707), (826, 702), (827, 701), (828, 705), (829, 706),
(830, 703), (831, 705), (832, 704), (833, 708), (834, 701),
(835, 706), (836, 702), (837, 705), (838, 703), (839, 704);

-- Bridge: CustomerClosetClothingItems
-- Placing the new items into the new closets (109-170)
-- 125+ rows
INSERT INTO CustomerClosetClothingItems (ClothingItemID, ClosetID, NumberofWears, AvailabilityStatus) VALUES
(820, 109, 5, TRUE), (821, 110, 10, TRUE), (822, 111, 2, FALSE),
(823, 112, 15, TRUE), (824, 113, 0, TRUE), (825, 114, 20, TRUE),
(826, 115, 1, TRUE), (827, 116, 8, TRUE), (828, 117, 3, FALSE),
(829, 118, 12, TRUE), (830, 119, 50, TRUE), (831, 120, 25, TRUE),
(832, 121, 6, TRUE), (833, 122, 4, FALSE), (834, 123, 9, TRUE),
(835, 124, 30, TRUE), (836, 125, 7, TRUE), (837, 126, 100, TRUE),
(838, 127, 14, TRUE), (839, 128, 2, TRUE), (840, 129, 11, FALSE),
(841, 130, 18, TRUE), (842, 131, 5, TRUE), (843, 132, 22, TRUE),
(844, 133, 1, TRUE), (845, 134, 3, TRUE), (846, 135, 8, TRUE),
(847, 136, 0, TRUE), (848, 137, 13, FALSE), (849, 138, 40, TRUE),
(850, 139, 2, TRUE), (851, 140, 6, TRUE), (852, 141, 9, TRUE),
(853, 142, 15, TRUE), (854, 143, 7, FALSE), (820, 144, 3, TRUE),
(821, 145, 11, TRUE), (822, 146, 4, TRUE), (823, 147, 8, TRUE),
(824, 148, 1, TRUE), (825, 149, 19, FALSE), (826, 150, 5, TRUE),
(827, 151, 12, TRUE), (828, 152, 2, TRUE), (829, 153, 7, TRUE),
(830, 154, 25, TRUE), (831, 155, 14, FALSE), (832, 156, 3, TRUE),
(833, 157, 6, TRUE), (834, 158, 8, TRUE), (835, 159, 21, TRUE),
(836, 160, 0, TRUE), (837, 161, 9, TRUE), (838, 162, 33, FALSE),
(839, 163, 4, TRUE), (840, 164, 10, TRUE), (841, 165, 2, TRUE),
(842, 166, 16, TRUE), (843, 167, 5, TRUE), (844, 168, 1, FALSE),
(845, 169, 7, TRUE), (846, 170, 12, TRUE), (847, 109, 3, TRUE),
(848, 110, 8, TRUE), (849, 111, 20, TRUE), (850, 112, 4, TRUE),
(851, 113, 1, FALSE), (852, 114, 6, TRUE), (853, 115, 9, TRUE),
(854, 116, 15, TRUE), (820, 117, 2, TRUE), (821, 118, 5, TRUE),
(822, 119, 11, FALSE), (823, 120, 7, TRUE), (824, 121, 3, TRUE),
(825, 122, 18, TRUE), (826, 123, 4, TRUE), (827, 124, 10, TRUE),
(828, 125, 1, FALSE), (829, 126, 6, TRUE), (830, 127, 22, TRUE),
(831, 128, 8, TRUE), (832, 129, 2, TRUE), (833, 130, 14, TRUE),
(834, 131, 5, TRUE), (835, 132, 9, FALSE), (836, 133, 3, TRUE),
(837, 134, 12, TRUE), (838, 135, 0, TRUE), (839, 136, 7, TRUE),
(840, 137, 16, TRUE), (841, 138, 4, TRUE), (842, 139, 1, FALSE),
(843, 140, 10, TRUE), (844, 141, 5, TRUE), (845, 142, 8, TRUE),
(846, 143, 2, TRUE), (847, 144, 6, TRUE), (848, 145, 13, TRUE),
(849, 146, 25, FALSE), (850, 147, 3, TRUE), (851, 148, 9, TRUE),
(852, 149, 11, TRUE), (853, 150, 4, TRUE), (854, 151, 7, TRUE),
(820, 152, 1, TRUE), (821, 153, 5, FALSE), (822, 154, 2, TRUE),
(823, 155, 15, TRUE), (824, 156, 8, TRUE), (825, 157, 3, TRUE),
(826, 158, 6, TRUE), (827, 159, 10, TRUE), (828, 160, 4, FALSE),
(829, 161, 12, TRUE), (830, 162, 1, TRUE), (831, 163, 7, TRUE),
(832, 164, 20, TRUE), (833, 165, 5, TRUE), (834, 166, 9, FALSE),
(835, 167, 2, TRUE), (836, 168, 11, TRUE), (837, 169, 6, TRUE);

-- Add some items to Rachel Green's wishlist (WishlistID 212)
INSERT INTO CustWishListClothingItem (ItemID, WishlistID, ClothingItemID) VALUES
(1, 212, 820), -- Vintage Silk Scarf
(2, 212, 843), -- Knee High Boots
(3, 212, 829), -- Pleated Tennis Skirt
(4, 212, 844); -- Baguette Bag