from polycule import Polycule, RegistrationError, RelationshipType
import os
import pytest

def test_complex_polycule():
    try:
        os.remove("1469403707920875560.gml")
    except:
        pass

    cule = Polycule(1469403707920875560)

    cule.register(795076172886048828, "Mixty", "She/They", "Puppycat")
    cule.register(981016097086132244, "Kira", "She/Her", "Kitty")
    cule.register(737492309234417664, "Lills", "She/They", "Fops")
    cule.register(257211665685282816, "Kaia", "She/Her", "Cat")
    cule.register(865853463160946708, "Sabrina", "She/Her", "Puppy")
    cule.register(274663332609392640, "Ellie", "She/Her", "Cat")
    cule.register(187705220757848064, "Cassie", "She/Her", "Doggo")
    cule.register(249744112901816321, "Daisy", "", "")
    cule.register(316290958452981762, "Polly", "", "")
    cule.register(275183183132229632, "Dizzy", "", "")
    cule.register(559845293517176852, "Savory", "", "")
    cule.register(156559749385682944, "Emmy", "", "")
    cule.register(396008675246080003, "Ellie", "", "")

    cule.add_relationship(795076172886048828, 981016097086132244, None, RelationshipType.Partner)
    cule.add_relationship(795076172886048828, 737492309234417664, None, RelationshipType.Partner)
    cule.add_relationship(257211665685282816, 737492309234417664, None, RelationshipType.Partner)
    cule.add_relationship(257211665685282816, 981016097086132244, None, RelationshipType.Partner)
    cule.add_relationship(257211665685282816, 865853463160946708, "Tmp Name", RelationshipType.Partner)
    cule.add_relationship(257211665685282816, 274663332609392640, None, RelationshipType.Partner)
    cule.add_relationship(865853463160946708, 274663332609392640, None, RelationshipType.Partner)

    cule.add_relationship(981016097086132244, 187705220757848064, None, RelationshipType.Partner)

    # TODO FIgure out a better way to handle duplicate names without unique IDs
    cule.add_relationship(981016097086132244, None, "Cass", RelationshipType.Partner)
    cule.add_relationship(187705220757848064, None, "Cass", RelationshipType.Partner)
    
    cule.add_relationship(274663332609392640, None, "Aspen", RelationshipType.FWB)
    cule.add_relationship(274663332609392640, 249744112901816321, None, RelationshipType.FWB)
    cule.add_relationship(316290958452981762, 865853463160946708, None, RelationshipType.Partner)

    cule.add_relationship(316290958452981762, None, 'Jess', RelationshipType.Partner)
    cule.add_relationship(187705220757848064, None, 'Bell', RelationshipType.Partner)
    cule.add_relationship(316290958452981762, None, 'Bell', RelationshipType.Partner)

    cule.add_relationship(865853463160946708,275183183132229632, None, RelationshipType.Partner)
    cule.add_relationship(559845293517176852,275183183132229632, None, RelationshipType.Married)
    cule.add_relationship(559845293517176852, None, 'Bike<3', RelationshipType.Partner)
    cule.add_relationship(559845293517176852, None, 'Hazel', RelationshipType.Dating)
    cule.add_relationship(275183183132229632, None, 'Vivienne', RelationshipType.Dating)
    cule.add_relationship(249744112901816321, None, 'Era', RelationshipType.Partner)
    cule.add_relationship(249744112901816321, None, 'Lilac', RelationshipType.Partner)
    cule.add_relationship(559845293517176852,865853463160946708, None,  RelationshipType.Dating)
    cule.add_relationship(274663332609392640,981016097086132244, None,  RelationshipType.Partner)
    cule.add_relationship(249744112901816321,257211665685282816, None,  RelationshipType.FWB)
    cule.add_relationship(249744112901816321,865853463160946708, None,  RelationshipType.FWB)
    cule.add_relationship(249744112901816321, None, 'Courtney', RelationshipType.Dating)
    cule.add_relationship(249744112901816321, None, 'James', RelationshipType.Dating)
    cule.add_relationship(737492309234417664, None, 'Millie', RelationshipType.Dating)
    cule.add_relationship(396008675246080003, None, 'Autium', RelationshipType.Partner)
    cule.add_relationship(396008675246080003,156559749385682944, None,  RelationshipType.Partner)
    cule.add_relationship(156559749385682944, None, 'Autium',RelationshipType.Partner)

    # Oddball folks
    # cule.add_relationship('long distance 1','Silent', RelationshipType.Unknown)
    # cule.add_relationship('long distance 2','Silent', RelationshipType.Unknown)
    # cule.add_relationship('long distance 3','Silent', RelationshipType.Unknown)
    # cule.add_relationship('Vi','Era', RelationshipType.Dating)
    # cule.add_relationship('Silent','Vivienne', RelationshipType.Partner)
    # cule.add_relationship('Jessie','Hazel', RelationshipType.Partner)
    # cule.add_relationship('Vivienne','Jessie', RelationshipType.Partner)
    # cule.add_relationship('Bell','Lydia', RelationshipType.FWB)

    cule.render_graph()

userId1 = 1234
userId2 = 4321
userId3 = 5678

userName1 = "user 1"
userName2 = "user 2"
userName3 = "user 3"

def test_add_relationship_without_registration():
    cule = Polycule(1)
    with pytest.raises(RegistrationError):
        cule.add_relationship(userId1, userId2, userName2, RelationshipType.Unknown)

def test_add_relationship_basic():
    cule = Polycule(1)
    cule.register(userId1, userName1)
    cule.add_relationship(userId1, userId2, None, RelationshipType.Unknown)

def test_add_relationship_partner_not_registered():
    cule = Polycule(1)
    cule.register(userId1, userName1)
    cule.add_relationship(userId1, userId2, None, RelationshipType.Unknown)
    with pytest.raises(RegistrationError):
        cule.add_relationship(userId2, userId3, None, RelationshipType.Unknown)

def test_add_relationship_no_id_basic():
    cule = Polycule(1)
    cule.register(userId1, userName1)
    cule.add_relationship(userId1, None, userName2, RelationshipType.Dating)

def test_get_relationships_basic():
    cule = Polycule(1)
    cule.register(userId1, userName1)
    cule.add_relationship(userId1, userId2, userName2, RelationshipType.Dating)

    partners = cule.get_relationships(userId1)
    assert partners.find(userName2) != -1

    partners = cule.get_relationships(userId2)
    assert partners.find(userName1) != -1
    