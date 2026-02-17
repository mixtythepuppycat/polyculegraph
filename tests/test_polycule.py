from polycule import Polycule, RegistrationError, RelationshipType
import os
import pytest

@pytest.fixture
def cule():
    cule = Polycule(12345678)
    yield cule
    # Remove the temporary file after the test
    if os.path.exists("12345678.gml"):
        os.remove("12345678.gml")

def test_complex_polycule(cule):
    cule.register(478931855585559369, "Mixty", "She/They", "Puppycat")
    cule.register(947083712350632235, "Kitty", "She/Her", "Kitty")
    cule.register(399212977380779689, "Foxy", "She/They", "Fops")
    cule.register(817575494082348732, "Cat Cat Cat", "She/Her", "Cat")
    cule.register(719239478925709211, "Puppy", "She/Her", "Puppy")
    cule.register(794486843458414444, "Ms Meow", "She/Her", "Cat")
    cule.register(465501736923208750, "Coyote", "She/Her", "Doggo")
    cule.register(582975770838924216, "Demon Dog", "", "")
    cule.register(201496998552537921, "Good Girl", "", "")
    cule.register(643515267028270322, "Right Round Baby", "", "")
    cule.register(477394836925609512, "OG Polygrapher", "", "")
    cule.register(431955697218180687, "Bunny", "", "")
    cule.register(346102910047043199, "Kitty Kat 2", "", "")

    cule.add_self_relationship(478931855585559369, 947083712350632235, None, RelationshipType.Partner)
    cule.add_self_relationship(478931855585559369, 399212977380779689, None, RelationshipType.Partner)
    cule.add_self_relationship(817575494082348732, 399212977380779689, None, RelationshipType.Partner)
    cule.add_self_relationship(817575494082348732, 947083712350632235, None, RelationshipType.Partner)
    cule.add_self_relationship(817575494082348732, 719239478925709211, "Tmp Name", RelationshipType.Partner)
    cule.add_self_relationship(817575494082348732, 794486843458414444, None, RelationshipType.Partner)
    cule.add_self_relationship(719239478925709211, 794486843458414444, None, RelationshipType.Partner)

    cule.add_self_relationship(947083712350632235, 465501736923208750, None, RelationshipType.Partner)

    cule.add_self_relationship(947083712350632235, None, "Dragon", RelationshipType.Partner)
    cule.add_self_relationship(465501736923208750, None, "Dragon", RelationshipType.Partner)
    
    cule.add_self_relationship(794486843458414444, None, "Colorado", RelationshipType.FWB)
    cule.add_self_relationship(794486843458414444, 582975770838924216, None, RelationshipType.FWB)
    cule.add_self_relationship(201496998552537921, 719239478925709211, None, RelationshipType.Partner)

    cule.add_self_relationship(201496998552537921, None, 'Mess', RelationshipType.Partner)
    cule.add_self_relationship(465501736923208750, None, 'Ring', RelationshipType.Partner)
    cule.add_self_relationship(201496998552537921, None, 'Ring', RelationshipType.Partner)

    cule.add_self_relationship(719239478925709211,643515267028270322, None, RelationshipType.Partner)
    cule.add_self_relationship(477394836925609512,643515267028270322, None, RelationshipType.Married)
    cule.add_self_relationship(477394836925609512, None, 'Bike<3', RelationshipType.Partner)
    cule.add_self_relationship(477394836925609512, None, 'Aqua', RelationshipType.Dating)
    cule.add_self_relationship(643515267028270322, None, 'Vi', RelationshipType.Dating)
    cule.add_self_relationship(582975770838924216, None, 'Arc', RelationshipType.Partner)
    cule.add_self_relationship(582975770838924216, None, 'Lavender', RelationshipType.Partner)
    cule.add_self_relationship(477394836925609512,719239478925709211, None,  RelationshipType.Dating)
    cule.add_self_relationship(794486843458414444,947083712350632235, None,  RelationshipType.Partner)
    cule.add_self_relationship(582975770838924216,817575494082348732, None,  RelationshipType.FWB)
    cule.add_self_relationship(582975770838924216,719239478925709211, None,  RelationshipType.FWB)
    cule.add_self_relationship(582975770838924216, None, 'Court', RelationshipType.Dating)
    cule.add_self_relationship(582975770838924216, None, 'Street', RelationshipType.Dating)
    cule.add_self_relationship(399212977380779689, None, 'Saw', RelationshipType.Dating)
    cule.add_self_relationship(346102910047043199, None, 'Spring', RelationshipType.Partner)
    cule.add_self_relationship(346102910047043199,431955697218180687, None,  RelationshipType.Partner)
    cule.add_self_relationship(431955697218180687, None, 'Spring',RelationshipType.Partner)

    # Relationships that are fully off the discord server
    cule.add_others_relationship(None, 'ld 1', None, 'Quiet', RelationshipType.Unknown)
    cule.add_others_relationship(None, 'ld 2', None, 'Quiet', RelationshipType.Unknown)
    cule.add_others_relationship(None, 'ld 3', None, 'Quiet', RelationshipType.Unknown)
    cule.add_others_relationship(None, 'Vi', None, 'Arc', RelationshipType.Dating)
    cule.add_others_relationship(None, 'Quiet', None, 'Vi', RelationshipType.Partner)
    cule.add_others_relationship(None, 'Tessie', None, 'Aqua', RelationshipType.Partner)
    cule.add_others_relationship(None, 'Vi', None, 'Tessie', RelationshipType.Partner)
    cule.add_others_relationship(None, 'Ring', None, 'Bettlejuice', RelationshipType.FWB)

    cule.render_graph_to_file()

    # See if we did anything to corrupt the on disk file by loading it again
    cule = Polycule(12345678)

    # Mixty
    relationships = cule.get_relationships(478931855585559369)
    assert "Kitty" in relationships
    assert "Foxy" in relationships

    # Kitty
    relationships = cule.get_relationships(947083712350632235)
    assert "Mixty" in relationships
    assert "Cat Cat Cat" in relationships
    assert "Ms Meow" in relationships
    assert "Coyote" in relationships
    assert "Dragon" in relationships

    # Foxy
    relationships = cule.get_relationships(399212977380779689)
    assert "Mixty" in relationships
    assert "Saw" in relationships
    assert "Cat Cat Cat" in relationships

    # Cat Cat Cat
    relationships = cule.get_relationships(817575494082348732)
    assert "Foxy" in relationships
    assert "Ms Meow" in relationships
    assert "Puppy" in relationships
    assert "Demon Dog" in relationships
    assert "Kitty" in relationships


userId1 = 1234
userId2 = 4321
userId3 = 5678

userName1 = "user 1"
userName2 = "user 2"
userName3 = "user 3"

def test_add_relationship_without_registration(cule):
    with pytest.raises(RegistrationError):
        cule.add_self_relationship(userId1, userId2, userName2, RelationshipType.Unknown)

def test_add_relationship_basic(cule):
    cule.register(userId1, userName1)
    cule.add_self_relationship(userId1, userId2, None, RelationshipType.Unknown)

def test_add_relationship_partner_not_registered(cule):
    cule.register(userId1, userName1)
    cule.add_self_relationship(userId1, userId2, None, RelationshipType.Unknown)
    with pytest.raises(RegistrationError):
        cule.add_self_relationship(userId2, userId3, None, RelationshipType.Unknown)

def test_add_relationship_no_id_basic(cule):
    cule.register(userId1, userName1)
    cule.add_self_relationship(userId1, None, userName2, RelationshipType.Dating)

def test_get_relationships_basic(cule):
    cule.register(userId1, userName1)
    cule.add_self_relationship(userId1, userId2, userName2, RelationshipType.Dating)

    partners = cule.get_relationships(userId1)
    assert partners.find(userName2) != -1

    partners = cule.get_relationships(userId2)
    assert partners.find(userName1) != -1