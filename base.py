import mysql.connector
from dotenv import load_dotenv
import os
import discord
import db_utils



if __name__ == "__main__":
    load_dotenv()

    token = os.getenv('TOKEN')

    bot = discord.Bot()

    conn = mysql.connector.connect(
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        host=os.getenv('HOST'),
        database = os.getenv('DATABASE'),
        auth_plugin='mysql_native_password')

    cursor = conn.cursor()

    @bot.slash_command(name = "check-social-points", description = "Check the points of the given user.")
    async def check_points(ctx, user: discord.User):
        
        points = await db_utils.check_user_points(cursor, user.id)

        if points == -1:
            await db_utils.add_new_user(conn, cursor, user.id)
            points = 1000

        conn.commit()

        embed = discord.Embed(
            title=f"{user.name}'s social points",
            description=f"{user.name.capitalize()} has a total of {points} social points.",
            color=discord.Colour.greyple(),
        )

        embed.set_thumbnail(url=user.avatar.url)


        await ctx.respond(embed=embed)

    @bot.slash_command(name = "give-or-take-points", description = "Give someone or take their social points.")
    async def give_take_points(ctx, user: discord.User, how_many_points: int):
        if ctx.author.guild_permissions.ban_members:
            points = await db_utils.check_user_points(cursor, user.id)

            if points == -1:
                await db_utils.add_new_user(conn, cursor, user.id)
                points = 1000
            else:
                await db_utils.update_user_points(conn, cursor, user.id, how_many_points)

            conn.commit()

            embed = discord.Embed(
                title=f"{user.name}'s social points",
                description=f"{user.name.capitalize()} now has {points+how_many_points} social points.",
                color=discord.Colour.brand_red(),
            )

            embed.set_thumbnail(url=user.avatar.url)

            await ctx.respond(embed=embed)
        else:
            await ctx.respond("You don't have permissions to give or take points from users.")


    @bot.slash_command(name = "social-points-leaderboard", description = "Display top 10 users with the highest, or the lowest amount of points.")
    async def best_worst_users(ctx, order: discord.Option(str, "Give the order either ASC or DESC", required=False, default="DESC")):
        top = await db_utils.top_10_users(conn, cursor, order)

        embed = discord.Embed(
        title="Top 10 users ",
        description=f"Top 10 in {order.lower()}ending order",
        color=discord.Colour.brand_green(),
    )

        for i, row in enumerate(top):
            user = await bot.fetch_user(row[0])
            embed.add_field(name=f"Number {i+1}:", value=f"{user.name} {row[1]}", inline=False)
        await ctx.respond(embed=embed) 


    bot.run(token)





