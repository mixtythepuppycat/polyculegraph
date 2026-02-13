from unittest.mock import Mock, AsyncMock
import pytest
import bot
from polycule import RelationshipType
from callee import Contains

@pytest.fixture
def mock_interaction() -> Mock:
    interaction = AsyncMock()
    return interaction

@pytest.fixture
def mock_member() -> Mock:
    member = Mock()
    return member

class any_string_with(str):
    def __eq__(self, other):
        return self in other

SUCCESS_MSG = "✅"
ERROR_MSG = "❌"

@pytest.mark.asyncio
async def test_add_partner_with__unregistered_discord_member(mock_interaction, mock_member):
    await bot._add_partner(mock_interaction, RelationshipType.Dating, partner=mock_member)
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(ERROR_MSG), ephemeral=True)

@pytest.mark.asyncio
async def test_add_partner_missing_parameters(mock_interaction):
    await bot._add_partner(mock_interaction, RelationshipType.Dating)
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(ERROR_MSG), ephemeral=True)

@pytest.mark.asyncio
async def test_add_partner_too_many_parameters(mock_interaction, mock_member):
    await bot._add_partner(mock_interaction, mock_member, "asdf", RelationshipType.Dating)
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(ERROR_MSG), ephemeral=True)

@pytest.mark.asyncio
async def test_registration(mock_interaction, mock_member):
    await bot._register(mock_interaction, preferred_name="Test User", pronouns="It/Its", critter_type="Robot")
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(SUCCESS_MSG))

@pytest.mark.asyncio
async def test_add_partner(mock_interaction, mock_member):    
    await bot._register(mock_interaction, preferred_name="Test User", pronouns="It/Its", critter_type="Robot")
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(SUCCESS_MSG))

    mock_interaction.reset_mock()
    await bot._add_partner(mock_interaction, RelationshipType.Dating, partner=mock_member)
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(SUCCESS_MSG))

@pytest.mark.asyncio
async def test_add_relationship(mock_interaction, mock_member):    
    await bot._add_relationship(mock_interaction, RelationshipType.Dating, person1_discord=mock_member, person2_discord=mock_member)
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(SUCCESS_MSG))

@pytest.mark.asyncio
async def test_add_relationship_with_missing_parameters(mock_interaction, mock_member):    
    await bot._add_relationship(mock_interaction, RelationshipType.Dating)
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(ERROR_MSG), ephemeral=True)

@pytest.mark.asyncio
async def test_add_relationship_with_too_parameters(mock_interaction, mock_member):    
    await bot._add_relationship(mock_interaction, RelationshipType.Dating, person1_discord=mock_member, 
                                person1_name="Test User 1", person2_discord=mock_member, person2_name="Test User 2")
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(ERROR_MSG), ephemeral=True)

@pytest.mark.asyncio
async def test_add_relationship_with_wrong_parameter_set(mock_interaction, mock_member):    
    await bot._add_relationship(mock_interaction, RelationshipType.Dating, person1_discord=mock_member, 
                                person1_name="Test User 1")
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(ERROR_MSG), ephemeral=True)

@pytest.mark.asyncio
async def test_remove_partner(mock_interaction, mock_member):
    await bot._register(mock_interaction, preferred_name="Test User", pronouns="It/Its", critter_type="Robot")
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(SUCCESS_MSG))

    mock_interaction.reset_mock()
    await bot._add_partner(mock_interaction, RelationshipType.Dating, partner=mock_member)
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(SUCCESS_MSG))

    mock_interaction.reset_mock()
    await bot._remove_partner(mock_interaction, mock_member)
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(SUCCESS_MSG), ephemeral=True)

@pytest.mark.asyncio
async def test_remove_partner_not_on_graph(mock_interaction, mock_member):
    await bot._register(mock_interaction, preferred_name="Test User", pronouns="It/Its", critter_type="Robot")
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(SUCCESS_MSG))

    mock_interaction.reset_mock()
    await bot._remove_partner(mock_interaction, mock_member)
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(ERROR_MSG), ephemeral=True)

@pytest.mark.asyncio
async def test_remove_partner_with_wrong_parameter_set(mock_interaction, mock_member):
    await bot._remove_partner(mock_interaction, mock_member, "Test User")
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(ERROR_MSG), ephemeral=True)

@pytest.mark.asyncio
async def test_unregister(mock_interaction):
    await bot._register(mock_interaction, preferred_name="Test User", pronouns="It/Its", critter_type="Robot")
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(SUCCESS_MSG))
    mock_interaction.reset_mock()

    await bot._unregister(mock_interaction, person_discord=mock_interaction.user)
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(SUCCESS_MSG))

@pytest.mark.asyncio
async def test_unregister_user_not_found(mock_interaction):
    await bot._unregister(mock_interaction, person_discord=mock_interaction.user)
    mock_interaction.response.send_message.assert_awaited_once_with(Contains(ERROR_MSG), ephemeral=True)