/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 100432 (10.4.32-MariaDB)
 Source Host           : localhost:3306
 Source Schema         : bytetalented

 Target Server Type    : MySQL
 Target Server Version : 100432 (10.4.32-MariaDB)
 File Encoding         : 65001

 Date: 31/05/2024 11:43:02
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tbl_bidlog
-- ----------------------------
DROP TABLE IF EXISTS `tbl_bidlog`;
CREATE TABLE `tbl_bidlog`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NULL DEFAULT 1,
  `apply_url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `company_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `position` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT current_timestamp,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_bidlog
-- ----------------------------
INSERT INTO `tbl_bidlog` VALUES (1, 1, 'asdf', 'asdfasdf', 'sadfsdf', '2024-05-27 20:34:01');
INSERT INTO `tbl_bidlog` VALUES (10, 1, 'https://docs.taipy.io/en/release-3.0/knowledge_base/tips/skippable_tasks/#use-caseasdf', 'Amateras', 'asdfsadf', '2024-05-28 03:51:30');
INSERT INTO `tbl_bidlog` VALUES (11, 1, 'https://docs.taipy.io/en/release-3.0/knowledge_base/tips/skippable_tasks/#use-case', 'Amateras', 'asdf', '2024-05-28 08:31:26');
INSERT INTO `tbl_bidlog` VALUES (12, 1, 'https://docs.taipy.io/en/release-3.0/knowaaaledge_base/tips/skippable_tasks/#use-caseffff', 'asdf', 'asdf', '2024-05-28 08:32:23');
INSERT INTO `tbl_bidlog` VALUES (13, 1, 'https://docs.taipy.io/en/release-3.0/knowaaaledge_base/tips/skippable_tasks/#use-case', 'aa', 'aa', '2024-05-28 08:32:27');
INSERT INTO `tbl_bidlog` VALUES (14, 0, 'https://taipy.io/book-a-call', 'taipy', 'Engineer', '2024-05-28 09:35:26');
INSERT INTO `tbl_bidlog` VALUES (15, 0, 'https://cli.github.com/', 'Github', 'Roll', '2024-05-28 09:35:47');

-- ----------------------------
-- Table structure for tbl_employee
-- ----------------------------
DROP TABLE IF EXISTS `tbl_employee`;
CREATE TABLE `tbl_employee`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `dob` date NULL DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `phone` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `address` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `id_front_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `id_back_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `selfie_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_employee
-- ----------------------------
INSERT INTO `tbl_employee` VALUES (2, 'Van Riet', '2024-05-06', 'abc@ab.com', '1 (234) 531-321', 'asdfasdf', 'fa96225c-dce2-46e3-83f2-6072779d6827.png', '3f6eb491-e6ec-42fa-acde-4bda7a752a86.jpg', 'a6fa49af-1928-4b12-b390-d8fd344d7653.mp4', 'asdfsdfsf');
INSERT INTO `tbl_employee` VALUES (3, 'Rand', '1994-05-11', 'rand.rand@rand.com', '1242 321 2414', 'gX 3203 UX American', 'd5e2335d-f521-409f-9b36-2a2cee35ea24.png', 'c2772330-156c-483b-9bbe-16cfb8a67da4.png', 'ca9d9aff-327e-4942-9f6a-b91840466d9c.mp4', 'Going....');
INSERT INTO `tbl_employee` VALUES (4, 'Rabeet', '1991-10-20', 'rabeet@gmail.com', '+86 (35) 421 2133', '1000 Faros Mumbai ', '8ba9c3a9-a97e-43e7-8aa3-a2355a4dc49e.jpeg', '11d8826c-dcc9-48fe-a40a-7b9addd258aa.png', 'cbd2c9b2-39e1-4c53-8842-d6cf0d5ad96c.mp4', 'Waiting');

-- ----------------------------
-- Table structure for tbl_support_candidate
-- ----------------------------
DROP TABLE IF EXISTS `tbl_support_candidate`;
CREATE TABLE `tbl_support_candidate`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `phone` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `position` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `photo_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 96 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_support_candidate
-- ----------------------------
INSERT INTO `tbl_support_candidate` VALUES (1, 'Anthony Cintron', 'anthony.cintron@gmail.com', ' 23423423424', 'FAFAfF', '11924cf9-626e-4c0a-9854-90521120882f.png');
INSERT INTO `tbl_support_candidate` VALUES (3, 'Anthony D. Mays', 'contact@anthonydmays.com', ' +1 (524) 224-2421', '  Software Engineer', 'b57a1b7a-f9a0-4ff4-b7e0-c1fa8ffab474.png');
INSERT INTO `tbl_support_candidate` VALUES (4, 'asdfasdfasdf', 'acd497@nyu.edu', ' ', '  ', 'a34893f6-601e-4e68-b299-94419aff3ad8.png');
INSERT INTO `tbl_support_candidate` VALUES (5, 'Anthony Salmeron', 'anthonysalmerondev@gmail.com', ' ', '  ', '642b6ebf-c130-4337-83f0-5425e8f48143.png');
INSERT INTO `tbl_support_candidate` VALUES (6, 'Antonio Rosales', 'a.webtone@gmail.com', ' ', '  ', 'cc4605c8-79b8-4da3-a70f-dea2077f2144.png');
INSERT INTO `tbl_support_candidate` VALUES (7, 'Apollo Emeka', 'apollo@apollostrategy.com', ' ', '  ', 'b3e1a1fd-0c05-496b-a782-87a28a07fcb0.png');
INSERT INTO `tbl_support_candidate` VALUES (8, 'Arcadio E. Quintero', 'oidacra@gmail.com', ' ', '  ', '4a2bdae3-9c59-49cf-8072-efe228b1fbf7.png');
INSERT INTO `tbl_support_candidate` VALUES (9, 'Looking for a job', 'ardaunverdi07@gmail.com', ' ', '  ', 'a6b6abae-14b1-4a49-b486-5944acad8e3e.png');
INSERT INTO `tbl_support_candidate` VALUES (10, 'Founder at Browse.ai', 'ardy@browse.ai', ' ', '  ', '372b733e-7d9f-4382-8ca3-956ac4e81d82.png');
INSERT INTO `tbl_support_candidate` VALUES (11, 'Arie Mangrum', 'arie.mangrum@kitcheck.com', ' ', '  ', '6b43da18-7e69-4d1e-ba57-f8d002e3c31b.png');
INSERT INTO `tbl_support_candidate` VALUES (12, 'Ariel Cascallares', 'arielcasca@gmail.com', '+5491122948076', '  ', 'e3c62f96-98c6-46f3-b9f5-b9946100096d.png');
INSERT INTO `tbl_support_candidate` VALUES (13, 'Arif Omanovié', 'arifom95@gmail.com', ' ', '  ', '4fc44f2a-6232-4d93-9bed-50f1d7363c86.png');
INSERT INTO `tbl_support_candidate` VALUES (14, 'Arlin Avery', 'arlin.avery@gmail.com', ' ', '  ', 'd184a241-c3c8-41cd-9b3c-3c8a7700047c.png');
INSERT INTO `tbl_support_candidate` VALUES (15, 'Armani Parker', 'armaniparker823@gmail.com', ' ', '  ', 'fc623336-40bb-4162-b015-845e519ad7ba.png');
INSERT INTO `tbl_support_candidate` VALUES (16, 'ASEFON PELUMI', 'pelumiasefon@gmail.com', ' ', '  ', 'fee6a93a-5a29-4245-8f9b-53669f68f75b.png');
INSERT INTO `tbl_support_candidate` VALUES (17, 'ashlon frank', 'frankashlon@gmail.com', ' ', '  ', '8a195fcb-5907-4092-ae63-f9ed00a920ee.png');
INSERT INTO `tbl_support_candidate` VALUES (18, 'Augustine Adugbe', 'adugbeaustin2@gmail.com', '+2347034608591', '  ', 'b71b6000-90c9-425d-942a-25dc4fd3f4c8.png');
INSERT INTO `tbl_support_candidate` VALUES (19, 'Augustine E.', '2403032@gmall.com', ' ', '  ', '627824a5-2f17-49b8-8b5f-90fbee72db7c.png');
INSERT INTO `tbl_support_candidate` VALUES (21, 'Avidan Attia', 'avidan@ownbackup.com', ' ', '  ', '78a215b6-7f46-46e0-8347-6685c774f9e6.png');
INSERT INTO `tbl_support_candidate` VALUES (22, 'Axel Esquite', 'aesquite@gmail.com', ' ', '  ', '10a06b32-7e1c-4f22-a40e-6489dd70a247.png');
INSERT INTO `tbl_support_candidate` VALUES (23, 'Ayabonga Booi', 'ayabongabooi2@gmail.com', ' ', '  ', '8c3e67ab-d281-4f42-b78a-092821c14d48.png');
INSERT INTO `tbl_support_candidate` VALUES (24, '© Invited member', 'ayantugaileolablessing442@gmail.com', ' ', '  ', '1d7ac861-3c7f-496b-8355-80dddb5cc7e2.png');
INSERT INTO `tbl_support_candidate` VALUES (25, 'Ayaz Azari', 'ayazazari7@gmail.com', ' ', '  ', '860367e7-ccda-45b3-bb93-378f15327ac5.png');
INSERT INTO `tbl_support_candidate` VALUES (26, 'Ayodeji Ajuwon', 'ajuwonayodeji.a@gmail.com', ' ', '  ', '2dea6c95-c944-4d0f-9c86-9459c20e52db.png');
INSERT INTO `tbl_support_candidate` VALUES (27, 'Ayoade Olayiwola', 'ayoadeolayiwola@gmail.com', ' ', '  ', '6b7c1703-8b3c-4375-89b5-e84cdffeefb0.png');
INSERT INTO `tbl_support_candidate` VALUES (28, 'Cd', 'yodeliolagbaiye@gmai.com', ' 09053526534', '  ', '0e62009d-5d38-43f2-a155-64d7ab8aa171.png');
INSERT INTO `tbl_support_candidate` VALUES (29, 'Ayomide Otukoya', 'yodeliolagbaiye@gmai.co', ' ', '  ', '301d00ac-8e97-47c3-bb75-c09059e17d2c.png');
INSERT INTO `tbl_support_candidate` VALUES (30, 'Azeem Abbas', 'azeem.abbas115@gmail.com', ' ', '  ', '8ba33764-4e6f-49ef-a563-17ce22762f63.png');
INSERT INTO `tbl_support_candidate` VALUES (31, 'Babajide Adebiyi', 'jeedeyy@gmail.com', ' 4349057330107', '  ', '61abdb89-fc10-4887-b618-09bfb33ee1e5.png');
INSERT INTO `tbl_support_candidate` VALUES (32, 'Bakari Akil', 'bakari@graveshallcap.com', ' ', '  ', '07f0b36e-36aa-4bac-a6b9-96c969a8b07e.png');
INSERT INTO `tbl_support_candidate` VALUES (33, 'Zed Robinson', 'services@zrobinson.com', ' asdfasdfsdf', '  ', '6d7351c6-a774-4951-b8d4-0f9118fb1013.png');
INSERT INTO `tbl_support_candidate` VALUES (34, 'Zachary Farris', 'farris@metadata.io', ' ', '  ', '90bd1873-bfd8-4e5c-8ec4-6426f4f47ada.png');
INSERT INTO `tbl_support_candidate` VALUES (35, 'Zach Wise-Copland', 'zachary.wise-copland@rsmus.com', ' ', '  ', '1736eed4-27cd-4283-8cbc-882216e841aa.png');
INSERT INTO `tbl_support_candidate` VALUES (36, 'Yusuf Gates', 'w3andapps@gmail.com', '+4407742484007', '  ', '204000e2-e3b2-411e-a508-57ecedbd48da.png');
INSERT INTO `tbl_support_candidate` VALUES (37, 'Yaw Afrifa', 'isaac.afrifa3@yahoo.com', ' ', '  ', '595979e0-eee1-469f-9b9c-a6b1a3259488.png');
INSERT INTO `tbl_support_candidate` VALUES (38, 'Yanny L Budiaki', 'ybu@container-xchange.com', ' ', '  ', '5cf708f7-6eaf-4945-81a1-e3abda18c9eb.png');
INSERT INTO `tbl_support_candidate` VALUES (39, 'Yannick Holton', 'holtonyannick@gmail.com', ' ', '  ', '9048eb9b-2ff7-4c04-9145-f37ccb56a1e3.png');
INSERT INTO `tbl_support_candidate` VALUES (40, 'Xevier Turrubiartes', 'xevier.dev@gmail.com', ' ', '  ', '7edb768b-853f-4dc8-8201-26f026fc415c.png');
INSERT INTO `tbl_support_candidate` VALUES (41, 'Xavier Shelley', 'xavier@candidate.co', ' ', '  ', 'a3870994-49dc-42b5-bd3d-8367d25d3a66.png');
INSERT INTO `tbl_support_candidate` VALUES (42, 'Vinicius Santos Guimaraes', 'vini65599@gmail.com', ' ', '', 'aeea7890-3e24-4732-b745-84b6e43e9285.png');
INSERT INTO `tbl_support_candidate` VALUES (43, 'Uton Keophila', 'uton.keophila@gmail.com', ' ', '', '43aeed34-2540-4efc-9497-826046712c1f.png');
INSERT INTO `tbl_support_candidate` VALUES (44, 'A', 'usaniewah@gmail.com', ' ', '  ', '136dae06-40e4-4efb-9996-2874cd3baa47.png');
INSERT INTO `tbl_support_candidate` VALUES (45, 'Usama Batavia', 'batavia_usama@hotmail.com', ' 6479857867', '  ', 'b6977502-81d9-446c-bade-b1b3e6c9e611.png');
INSERT INTO `tbl_support_candidate` VALUES (46, 'uriel karerwa', 'karerwau@gmail.com', ' ', '  ', 'd8dd84c1-77f5-48a5-abd4-7646f3b5a12e.png');
INSERT INTO `tbl_support_candidate` VALUES (47, 'UGOCHUKWU LAWRENCE', 'ugolawrence21@gmail.com', ' 08106062164', '  ', '8f469789-c3e3-406b-987a-c40a11e14c55.png');
INSERT INTO `tbl_support_candidate` VALUES (48, 'Uche Ogobegwu', 'ucheogobegwu@gmail.com', ' ', '  ', 'ffcad0be-8d86-4901-a771-706f0ba81677.png');
INSERT INTO `tbl_support_candidate` VALUES (49, 'Tyson M. Campbell', 'campbell97t@gmail.com', ' ', '  ', '55774d97-360f-402a-a163-3232649c7402.png');
INSERT INTO `tbl_support_candidate` VALUES (50, 'Tyreek Houston', 'tyreek.rh@gmai.com', ' ', '  ', '0c534bb7-23ef-479d-852b-8b0693f5e1ed.png');
INSERT INTO `tbl_support_candidate` VALUES (51, '', 'tyler@falkon.ai', ' ', '  ', '0d48d315-24d2-49e8-9ea9-327f20404c9f.png');
INSERT INTO `tbl_support_candidate` VALUES (52, 'Tyler Robinson', '.tyler.a@gmail.com', ' ', '  ', 'e0b0d45a-7c31-4fcf-be98-20fcc4a6286c.png');
INSERT INTO `tbl_support_candidate` VALUES (53, 'Tunde', 'toyedeji@gmail.com', ' ', '  ', '09e2a24f-e1ae-4568-9e87-26a5aced98a3.png');
INSERT INTO `tbl_support_candidate` VALUES (54, 'Tristan Pennicott', 'tpennicott@gmail.com', ' ', '  ', '7827fc15-bd88-432a-9bbe-184def0c60c7.png');
INSERT INTO `tbl_support_candidate` VALUES (55, 'Travis Lark', ' ', ' ', '  ', 'cbc8d822-3fd9-40b0-bd64-de6e8ce3aeb5.png');
INSERT INTO `tbl_support_candidate` VALUES (56, 'Travis Johnson', 'johnsontravis21@gmail.com', ' ', '  ', '9a91877f-d37c-4d48-afb1-2d9c90977828.png');
INSERT INTO `tbl_support_candidate` VALUES (57, 'Travis Flake', 'tflake83@gmail.com', ' ', '  ', 'e5192f84-606c-47d3-9fbd-2a3fc38f7f2e.png');
INSERT INTO `tbl_support_candidate` VALUES (58, 'Tracy Woods', 'woods304@gmai.com', ' ', '  ', '535495f5-9196-464a-ae48-d2985e3b7cb2.png');
INSERT INTO `tbl_support_candidate` VALUES (59, 'Tornike', 'qurdadzze@gmail.com', ' ', '  ', 'd90720a0-ecb8-4f20-80ca-f1b484433e82.png');
INSERT INTO `tbl_support_candidate` VALUES (60, 'Tony Ortiz', 'tony@tothedesigner.com', ' ', '  ', '73e59fe5-e109-4439-a8da-87064b743866.png');
INSERT INTO `tbl_support_candidate` VALUES (61, 'Tony DeLisio', 'tony.delisio@gmail.com', ' ', '  ', 'eaa839f3-b4f6-43b8-93b0-4e33ead94de7.png');
INSERT INTO `tbl_support_candidate` VALUES (62, 'Tonatiuh Jimenez', 'tonykurosaki117@gmail.com', ' ', '  ', '33469a84-f508-45e9-b203-46f7e00e7590.png');
INSERT INTO `tbl_support_candidate` VALUES (63, 'Tommy Adeniyi', 'tommyadeniyi@gmail.com', ' ', '  ', '854774d4-1862-4b9d-ae1a-3a09ab9c77c6.png');
INSERT INTO `tbl_support_candidate` VALUES (64, 'Tolu Bankole', 'ope.bankole.tolu@gmail.com', ' ', '  ', 'ac52b2a6-cd6c-4bf6-90f7-a7b321400a51.png');
INSERT INTO `tbl_support_candidate` VALUES (65, '© 3:26 PM local time', 'mtidowu@gmail.com', ' ', '  ', '5f3b2089-c326-48ea-8813-05d9d5aa1262.png');
INSERT INTO `tbl_support_candidate` VALUES (66, 'Todd Mann MBA, Ed.D', 'todd@chatbotgeniusllc.com', ' ', '  ', '58e28b07-6358-4288-a678-0f9e8b722649.png');
INSERT INTO `tbl_support_candidate` VALUES (67, 'Tito Zamalloa', 'tito.zamalloa@gmail.com', ' ', '  ', '99e0b076-471a-4e77-b851-37af19304e4d.png');
INSERT INTO `tbl_support_candidate` VALUES (68, 'Tirrell Cooper', 'tirrell.m.cooper@gmail.com', ' ', '  ', '5a0cce3e-a1c1-47f1-a749-4037c6eaeb43.png');
INSERT INTO `tbl_support_candidate` VALUES (69, 'Timothy Johnson', 'tiohnson3@gmail.com', ' ', '  ', 'faa9e399-a368-4655-86b6-8e54cfd3be33.png');
INSERT INTO `tbl_support_candidate` VALUES (70, 'Tim Alexander', 'tim.alexander@syncfoundry.com', ' ', '  ', '5ab96a42-78bd-44dc-a2e6-2c860edfc60e.png');
INSERT INTO `tbl_support_candidate` VALUES (71, '', 'teejay303@gmail.com', ' ', '  ', '2505ba43-b1fd-4d6f-ac6a-67d6a6bf8270.png');
INSERT INTO `tbl_support_candidate` VALUES (72, 'Tikere Ralands', 'tikere.ralands@voxmedia.com', ' ', '  ', '9812b07a-d53d-44c0-98c5-c7ead41cbd16.png');
INSERT INTO `tbl_support_candidate` VALUES (73, 'Tiffany Young', 'tiffanyyoungmpa@gmail.com', '2525066571', '  ', '49ead0a6-74c2-45d8-aa1b-cc9f4ba406bc.png');
INSERT INTO `tbl_support_candidate` VALUES (74, 'Tiffany', 'hello@tiffanyapril.co', ' ', '  ', '543d0a98-dd51-4d1b-adb4-0e4229478182.png');
INSERT INTO `tbl_support_candidate` VALUES (75, 'Tiara Mack', 'tiaramack@mentorcollective.org', ' ', '  ', '75cdbb17-6a68-4e57-87c8-557dc48caf66.png');
INSERT INTO `tbl_support_candidate` VALUES (76, 'Tieliek Curry', 'tieliek7@gmail.com', ' ', '  ', 'a8783e6c-655c-4145-b3c6-50afa660c46f.png');
INSERT INTO `tbl_support_candidate` VALUES (77, 'Tia Green', 'tialatricegreen@gmail.com', ' ', '  ', 'aef68d9c-0dd0-422c-a634-91a45f1e139b.png');
INSERT INTO `tbl_support_candidate` VALUES (78, 'Thompson Marzagao', 'marzagao@gmail.com', ' ', '  ', '982eb132-b3cd-4188-9911-9104114ed2eb.png');
INSERT INTO `tbl_support_candidate` VALUES (79, 'Thomas Yung', 'thomasyung@gmail.com', ' ', '  ', 'a6cfe8ef-15de-4f74-b2ac-0f1bb14a5ea2.png');
INSERT INTO `tbl_support_candidate` VALUES (80, 'Themba Msiza', 'timzworld@gmail.com', ' ', '  ', '6a970c6b-b410-4552-af43-e6c669aa32ca.png');
INSERT INTO `tbl_support_candidate` VALUES (81, 'TheGreatLouie', 'mrluisvicente@gmail.com', ' ', '  ', 'f9ec4079-449d-4353-887d-49f379fa8f4e.png');
INSERT INTO `tbl_support_candidate` VALUES (82, 'Thato Mahloko', 'thato732mahloko@gmail.com', ' ', '  ', 'b138969a-99e4-4409-8dd9-35837576ab69.png');
INSERT INTO `tbl_support_candidate` VALUES (83, 'Tevin Noel', 'tnoel.work@gmail.com', ' ', '  ', '774b386c-38ff-449a-8033-9ffef2257121.png');
INSERT INTO `tbl_support_candidate` VALUES (84, 'Terry Threatt', 'terry.threatt@gmail.com', ' ', '  ', 'ec5e4059-ab23-4aeb-8e80-4853d4749e51.png');
INSERT INTO `tbl_support_candidate` VALUES (85, 'Terry Mafura', 'maffsojah1@gmail.com', ' ', '  ', '877ccf68-a116-4e3f-b166-cc14d0643b2a.png');
INSERT INTO `tbl_support_candidate` VALUES (86, 'Terry', 'jr77@gmail.com', ' ', '  ', '23d744e8-ce72-4927-ac26-ba75f5a5e4e5.png');
INSERT INTO `tbl_support_candidate` VALUES (87, 'See ews er', 'terrancerange@gmail.com', ' ', '  ', '154494f4-8e44-4c36-8790-c0391454f90c.png');
INSERT INTO `tbl_support_candidate` VALUES (88, 'Terrall Jordan', 'terrall.jordan@gmail.com', ' ', '  ', '4e6286da-110c-4118-99d4-6421af36bf5d.png');
INSERT INTO `tbl_support_candidate` VALUES (89, 'Teresa Aportela Sergott', 'teresa.sergott@gmail.com', ' ', '  ', 'a0a9e1fa-03a5-4ede-a81b-584352f5366d.png');
INSERT INTO `tbl_support_candidate` VALUES (90, 'Tenzin Tsephel', 'tenzintsephel25@gmail.com', ' ', '  ', '556922e9-b3b8-4537-a8ed-c9a63c20ea10.png');
INSERT INTO `tbl_support_candidate` VALUES (91, 'Tennile', 'tennile@sheisepic.com', ' ', '  ', 'bbd1c3cd-304d-48dd-a3bf-a198af5b7961.png');
INSERT INTO `tbl_support_candidate` VALUES (92, 'Temi Wright', 'temi.wright@gmail.com', ' ', '  ', '86c3d38c-ef36-4ea5-94dd-d50f88080fd3.png');
INSERT INTO `tbl_support_candidate` VALUES (93, 'Teddy LaGuerre', 'laguerre.teddy@gmail.com', ' ', '  ', '586e46b4-075e-48af-8cd0-5756782f3772.png');
INSERT INTO `tbl_support_candidate` VALUES (94, 'Tapiwanashe Shoshore', 'tapsshore@gmail.com', ' ', '  ', '3c883775-2d25-4349-95b2-33c097cc7838.png');
INSERT INTO `tbl_support_candidate` VALUES (95, 'Tamzidul Matin', 'tmatin100@gmail.com', ' ', '  ', 'a333cc3e-82ee-4b94-a8e3-2b500b2156bf.png');

-- ----------------------------
-- Table structure for tbl_user
-- ----------------------------
DROP TABLE IF EXISTS `tbl_user`;
CREATE TABLE `tbl_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `role` int NULL DEFAULT 1,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_user
-- ----------------------------
INSERT INTO `tbl_user` VALUES (1, 'softdev019@gmail.com', '$2b$12$hYr2xQdhOO0Fxy9iCv.H6.sC4uTYd04La4qAbc2O8xk49CpxmIUMK', 1);
INSERT INTO `tbl_user` VALUES (2, 'asdf9@gmail.com', '$2b$12$k2yf7inMyVwzzjfskYRs7.mQK3tECN5LET2CwI6xVGaEVrlTbhdCC', 1);

-- ----------------------------
-- Table structure for tbl_user_city
-- ----------------------------
DROP TABLE IF EXISTS `tbl_user_city`;
CREATE TABLE `tbl_user_city`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NULL DEFAULT NULL,
  `city` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `country` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `timezone` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_user_city
-- ----------------------------
INSERT INTO `tbl_user_city` VALUES (2, 1, 'London', 'UK', 'Europe/London');
INSERT INTO `tbl_user_city` VALUES (3, 1, 'Tokyo', 'Japan', 'Asia/Tokyo');
INSERT INTO `tbl_user_city` VALUES (6, 1, 'Perth', 'Australia', 'Australia/Perth');
INSERT INTO `tbl_user_city` VALUES (7, 1, 'Beijing', 'China', 'Asia/Shanghai');
INSERT INTO `tbl_user_city` VALUES (8, 1, 'Rome', 'Italy', 'Europe/Rome');

SET FOREIGN_KEY_CHECKS = 1;
