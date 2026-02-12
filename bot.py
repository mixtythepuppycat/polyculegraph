import discord
from discord import app_commands
from keys import BOT_TOKEN
from logger import getLogger
import polycule
from polycule import Polycules, RegistrationError, RelationshipType

_log = getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
polycules = Polycules()

@tree.command(
    description="Add your partner",
    guild=discord.Object(id=1469403707920875560)
)
@app_commands.describe(partner="Your partner's Discord name",
                       relationship_type="What type of relationship is this?")
async def add_partner(interaction: discord.Interaction, partner: discord.Member, relationship_type: RelationshipType):
        try:
            polycules.get(interaction.guild_id).add_relationship(interaction.user.id, interaction.user.display_name, partner.id, partner.display_name, relationship_type)
            await interaction.response.send_message(f"✅ I added {partner} as your partner! ✅")
        except RegistrationError:
            await interaction.response.send_message("❌ ERROR: Please use /register before adding a partner ❌", ephemeral=True)

@tree.command(
    description="Remove a partner",
    guild=discord.Object(id=1469403707920875560)
)
@app_commands.describe(partner="Your former partner's Discord name")
async def remove_partner(interaction: discord.Interaction, partner: discord.Member):
        polycules.get(interaction.guild_id).remove_relationship(interaction.user.id, partner.id)
        await interaction.response.send_message(f"I removed {partner} as your partner", ephemeral=True)

@tree.command(
    description="Add a partner who's not on this server",
    guild=discord.Object(id=1469403707920875560)
)
@app_commands.describe(partner_name="Your partner's name",
                       relationship_type="What type of relationship is this?")
async def add_offserver_partner(interaction: discord.Interaction, partner_name: str, relationship_type: RelationshipType):
        polycules.get(interaction.guild_id).add_relationship(interaction.user.id, interaction.user.display_name, None, partner_name, relationship_type)
        await interaction.response.send_message(f"✅ I added {partner_name} as your partner! ✅")

@tree.command(
    description="Remove a partner who's not on this server",
    guild=discord.Object(id=1469403707920875560)
)
@app_commands.describe(partner_name="Your former partner's name")
async def remove_offserver_partner(interaction: discord.Interaction, partner_name: str):
        polycules.get(interaction.guild_id).remove_relationship(interaction.user.id, partner_name, False)
        await interaction.response.send_message(f"I removed {partner_name} as your partner", ephemeral=True)

@tree.command(
    description="View your registered partners",
    guild=discord.Object(id=1469403707920875560)
)
async def view_partners(interaction: discord.Interaction):
        partners = polycules.get(interaction.guild_id).get_relationships(interaction.user.id)
        await interaction.response.send_message(partners, ephemeral=True)

@tree.command(
    description="View your polycule's graph",
    guild=discord.Object(id=1469403707920875560)
)
async def view_polycule(interaction: discord.Interaction):
        graph = polycules.get(interaction.guild_id).render_graph()
        await interaction.response.send_message("HTML Done", ephemeral=True)

@tree.command(
    description="Register yourself with the polycule. Setup your preferred name, pronouns, and critter type",
    guild=discord.Object(id=1469403707920875560)
)
@app_commands.describe(preferred_name="The name you wish to display on the graph for yourself",
                       pronouns="Your pronouns",
                       critter_type="What type of critter are you? (Puppy, cat, fox, etc)")

async def register(interaction: discord.Interaction, preferred_name: str, pronouns: str = None, critter_type: str = None):
        polycules.get(interaction.guild_id).register(interaction.user.id, preferred_name, pronouns, critter_type)
        await interaction.response.send_message(f"✅ {preferred_name} been added to the polycule! ✅")

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1469403707920875560))
    print(f'We have logged in as {client.user}')

_log.info("STARTING BOT")
client.run(BOT_TOKEN)