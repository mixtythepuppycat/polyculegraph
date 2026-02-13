import discord
from discord import app_commands
from keys import BOT_TOKEN, URL_HOST
from logger import getLogger
from polycule import Polycules, RegistrationError, RelationshipType, NodeNotFound

_log = getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
polycules = Polycules()

POLYCULE_ADMIN_ROLE = "Polygrapher"

async def on_tree_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole):
        return await interaction.response.send_message(f"You require the {POLYCULE_ADMIN_ROLE} role to run this command.", ephemeral=True)
    else:
        raise error

tree.on_error = on_tree_error

@tree.command(description="Add your partner")
@app_commands.describe(partner="Your partner's Discord name",
                       partner_name="Your partner's name (only use if they aren't on this server)",
                       relationship_type="What type of relationship is this?")
async def add_partner(interaction: discord.Interaction, relationship_type: RelationshipType, partner: discord.Member = None, partner_name: str = None):
    await _add_partner(interaction, relationship_type, partner, partner_name)

async def _add_partner(interaction: discord.Interaction, relationship_type: RelationshipType, partner: discord.Member = None, partner_name: str = None):
    if partner is not None and partner_name is not None:
        await interaction.response.send_message("❌ ERROR: Please use either partner or partner_name and not both ❌", ephemeral=True)
    elif partner is None and partner_name is None:
        await interaction.response.send_message("❌ ERROR: Please use either partner or partner_name ❌", ephemeral=True)
    else:
        try:
            if partner:
                polycules.get(interaction.guild_id).add_self_relationship(interaction.user.id, partner.id, partner.display_name, relationship_type)
            else:
                polycules.get(interaction.guild_id).add_self_relationship(interaction.user.id, None, partner_name, relationship_type)

            await interaction.response.send_message(f"✅ I added {partner} as your partner! ✅")
        except RegistrationError:
            await interaction.response.send_message("❌ ERROR: Please use /register before adding a partner ❌", ephemeral=True)


@tree.command(description="Add a relationship to the polycule graph that is not your own.")
@app_commands.describe(person1_discord="The first person's Discord name",
                       person1_name="The first person's name (only use if they aren't on this server and not in combination with person1_discord)",
                       person2_discord="The second person's Discord name",
                       person2_name="The second person's name (only use if they aren't on this server and not in combination with person2_discord)",
                       relationship_type="What type of relationship is this?")
@app_commands.checks.has_role(POLYCULE_ADMIN_ROLE)
async def add_relationship(interaction: discord.Interaction, relationship_type: RelationshipType, person1_discord: discord.Member = None, 
                           person1_name: str = None, person2_discord: discord.Member = None, person2_name: str = None):
    await _add_relationship(interaction, relationship_type, person1_discord, person1_name, person2_discord, person2_name)

async def _add_relationship(interaction: discord.Interaction, relationship_type: RelationshipType, person1_discord: discord.Member = None, 
                           person1_name: str = None, person2_discord: discord.Member = None, person2_name: str = None):
    if person1_discord is not None and person1_name is not None:
        await interaction.response.send_message("❌ ERROR: Please use either person1_discord or person1_name and not both ❌", ephemeral=True)
    elif person2_discord is not None and person2_name is not None:
        await interaction.response.send_message("❌ ERROR: Please use either person2_discord or person2_name and not both ❌", ephemeral=True)
    elif person1_discord is None and person1_name is None:
        await interaction.response.send_message("❌ ERROR: Please use either person1_discord or person1_name ❌", ephemeral=True)
    elif person2_discord is None and person2_name is None:
        await interaction.response.send_message("❌ ERROR: Please use either person2_discord or person2_name ❌", ephemeral=True)
    else:
        person1_id = None
        person2_id = None
        if person1_discord:
            person1_id = person1_discord.id
            person1_name = person1_discord.display_name

        if person2_discord:
            person2_id = person2_discord.id
            person2_name = person2_discord.display_name

        polycules.get(interaction.guild_id).add_others_relationship(person1_id, person1_name, person2_id, person2_name, relationship_type)
        await interaction.response.send_message(f"✅ {person1_name}'s relationship with {person2_name} has been registered! ✅")

@tree.command(description="Remove a partner")
@app_commands.describe(partner="Your former partner's Discord name",
                       partner_name="Your former partner's name (only use if they aren't on this server)")
async def remove_partner(interaction: discord.Interaction, partner: discord.Member = None, partner_name: str = None):
    await _remove_partner(interaction, partner, partner_name)

async def _remove_partner(interaction: discord.Interaction, partner: discord.Member = None, partner_name: str = None):
    if partner is not None and partner_name is not None:
        await interaction.response.send_message("❌ ERROR: Please use either partner or partner_name ❌", ephemeral=True)
    else:
        try:
            if partner:
                partner_name = partner.id
            polycules.get(interaction.guild_id).remove_relationship(interaction.user.id, partner_name)

            await interaction.response.send_message(f"✅ I removed {partner} as your partner", ephemeral=True)
        except NodeNotFound as e:
            await interaction.response.send_message(f"❌ ERROR: {e} ❌", ephemeral=True)

@tree.command(description="View your registered partners")
async def view_partners(interaction: discord.Interaction):
        partners = polycules.get(interaction.guild_id).get_relationships(interaction.user.id)
        await interaction.response.send_message(partners, ephemeral=True)


@tree.command(description="View your polycule's graph")
async def view_polycule(interaction: discord.Interaction):
        # TODO Dynamic saves
        polycules.get(interaction.guild_id).render_graph_to_file()
        await interaction.response.send_message(f"{URL_HOST}/polycule/{interaction.guild_id}", ephemeral=True)


@tree.command(description="Register yourself with the polycule. Setup your preferred name, pronouns, and critter type")
@app_commands.describe(preferred_name="The name you wish to display on the graph for yourself",
                       pronouns="Your pronouns",
                       critter_type="What type of critter are you? (Puppy, cat, fox, etc)")
async def register(interaction: discord.Interaction, preferred_name: str, pronouns: str = None, critter_type: str = None):
    await _register(interaction, preferred_name, pronouns, critter_type)

async def _register(interaction: discord.Interaction, preferred_name: str, pronouns: str = None, critter_type: str = None):
    polycules.get(interaction.guild_id).register(interaction.user.id, preferred_name, pronouns, critter_type)
    await interaction.response.send_message(f"✅ {preferred_name} been added to the polycule! ✅")

@tree.command(description="Remove a person from the polycule graph")
@app_commands.describe(person_discord="The person's Discord name who is being removed",
                       person_name="The person's name who is being removed (only use if they aren't on this server)")
@app_commands.checks.has_role(POLYCULE_ADMIN_ROLE)
async def unregister(interaction: discord.Interaction, person_discord: discord.Member = None, person_name: str = None):
    await _unregister(interaction, person_discord, person_name)

async def _unregister(interaction: discord.Interaction, person_discord: discord.Member = None, person_name: str = None):
    if person_discord:
        person_name = person_discord.id
    
    try:
        polycules.get(interaction.guild_id).unregister(person_name)
        await interaction.response.send_message(f"✅ {person_name} has been removed from the polycule! ✅")
    except NodeNotFound as e:
        await interaction.response.send_message(f"❌ ERROR: {e} ❌", ephemeral=True)

@client.event
async def on_ready():
    await tree.sync()
    print(f'We have logged in as {client.user}')

if __name__ == '__main__':
    _log.info("STARTING BOT")
    client.run(BOT_TOKEN)