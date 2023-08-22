import time
import discord
from discord.ext import commands
import smtplib
import random
import email.message
import pandas as pd
import datetime
import asyncio

def verificar_email(x, email_, nome, email_prof, nome_prof):  # Verifica se o email fornecido consta no banco de dados e retorna o nome completo do usuário associado
    print(x)
    for i in email_:
        if i == x:
            print("Aluno autenticado.")
            print(nome[email_.index(i)])
            return nome[email_.index(i)]

    for i in email_prof:
        if x == i:
            print("Professor autenticado.")
            print(nome_prof[email_prof.index(i)])
            return nome_prof[email_prof.index(i)]
    print("Usuário não consta no banco de dados. Verifique se a escrita e tente novamente.")

emails_alunos = [] #Emails institucionais dos alunos.
nomes_alunos = [] #Nomes completos dos alunos
emails_professores = [] #Emails institucionais dos professores
nomes_professores = [] #Nomes completos dos professores

planilha_alunos = pd.read_csv(r"C:\Users\marco\OneDrive\Área de Trabalho\Faculdade\Algoritmos e programação\Projeto - Algoritmos e  Programação\alunos.csv")
planilha_professores = pd.read_csv(r"C:\Users\marco\OneDrive\Área de Trabalho\Faculdade\Algoritmos e programação\Projeto - Algoritmos e  Programação\professores.csv")

for indice, linha in planilha_alunos.iterrows(): #lê a planilha com os dados e guarda nomes e emails nas respectivas listas.
    emails_alunos.append(linha[7])
    nomes_alunos.extend([linha[1]])

for indice, linha in planilha_professores.iterrows(): #lê a planilha com os dados e guarda nomes e emails nas respectivas listas.
    nomes_professores.extend([linha[0]])
    emails_professores.extend([linha[1]])

intents = discord.Intents.all()
client = commands.Bot(command_prefix="", intents=intents)  # aqui definimos qual o prefixo que vamos utilizar na execução de comandos

listaD = ['marcosbelods@gmail.com', 'paulimskt1213@gmail.com']  # lista especial com e-mail dos desenvolvedores do bot
listaC = ['henrique.cunha@ifpb.edu.br']
cargo = False

@client.event
async def on_guild_join(guild):

    # pegando o canal inicial
    canal_inicial = guild.text_channels[0]

    # Define o canal inicial
    await guild.edit(system_channel=canal_inicial)


@client.event  # evento que adciona automaticamente o cargo de pretendente para um novo usuário
async def on_member_join(member):
    username = member.name
    role_id = 1116342323975045231
    role = discord.utils.get(member.guild.roles, id=int(role_id))
    await member.add_roles(role)
    a = datetime.datetime.now()
    a = str(a)
    b = a[11:16]
    print("O membro %s entrou no servidor as %s hrs" % (username,b))
    channel_id = 1117801654633373820
    channel = client.get_channel(channel_id)
    b = float(a[11] + a[12] + "." +a[14] + a[15])

    if 4 < b < 12:
        await channel.send('Bom dia! Seja bem-vindo, ' + username + '!')
        await asyncio.sleep(1)
        await channel.send('Eu sou o bot desenvolvido pelos alunos do curso para automatizar a experiência do usuário no servidor.')
        await asyncio.sleep(3)
        await channel.send('Primeiramente, por meio deste canal vamos autenticar o seu acesso ao servidor')
        await asyncio.sleep(2)
        await channel.purge(limit=None)

    elif 12 <= b < 18:
        await channel.send('Boa tarde! Seja bem-vindo, ' + username + '!')
        await asyncio.sleep(1)
        await channel.send('Eu sou o bot desenvolvido pelos alunos do curso para automatizar a experiência do usuário no servidor.')
        await asyncio.sleep(3)
        await channel.send('Primeiramente, por meio deste canal vamos autenticar o seu acesso ao servidor')
        await asyncio.sleep(2)
        await channel.purge(limit=None)

    elif 18 <= b <=23 or 00 <= b < 5 :
        await channel.send('Boa noite! Seja bem-vindo, ' + username + '!')
        await asyncio.sleep(1)
        await channel.send('Eu sou o bot desenvolvido pelos alunos do curso para automatizar a experiência do usuário no servidor.')
        await asyncio.sleep(3)
        await channel.send('Primeiramente, por meio deste canal vamos autenticar o seu acesso ao servidor')
        await asyncio.sleep(2)
        await channel.purge(limit=None)

    await asyncio.sleep(0)
    embed = discord.Embed(title='Qual é o seu cargo na instituição atualmente?',description='Assinale dentre as opções abaixo:', color=discord.Color.blue())
    embed.add_field(name='1- Aluno/Professor', value='Discente/Doscente do curso de Engenharia de Computação.', inline=False)
    embed.add_field(name='2 - Egresso', value='Ex-Aluno concluinte do curso de Engenharia de Computação.', inline=False)

    channel_id = 1117801654633373820
    channel = client.get_channel(channel_id)
    message = await channel.send(embed=embed)
    await message.add_reaction('1️⃣')
    await message.add_reaction('2️⃣')

@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    canal = str(channel)
    member = reaction.message.guild.get_member(user.id)

    if str(reaction.emoji) == '1️⃣' and member.bot == False and canal == "autenticação":
        print("%s reagiu no canal %s"%(member,canal))
        await channel.send(f'{member.name} escolheu a opção Aluno/Professor.')
        await reaction.message.delete()
        await asyncio.sleep(3)
        await channel.purge(limit=None)
        await channel.send('Agora, me envie seu email institucional para que possamos continuar')
        print("reação recebida")

    elif str(reaction.emoji) == '2️⃣' and member.bot == False and canal == "autenticação":
        await channel.send(f'{member.name} escolheu a opção Egresso.')
        await reaction.message.delete()
        await asyncio.sleep(3)
        await channel.purge(limit=None)
        await channel.send('Agora, me envie seu nome completo, ano de conclusão, sua data de nascimento e e-mail de contato como mostra o modelo a seguir: "Nome, ano de conclusão, data de nascimento, e-mail"')
        print("reação recebida")


    elif str(reaction.emoji) == '👍' and member.bot == False and canal == "coordenador_egressos":
        print("autorizado")
        lista = client.get_channel(1120674093159690310)
        users = lista.members
        user = users[-1]
        print(user)
        role = user.guild.get_role(1116342197638414437)
        role2 = user.guild.get_role(1120911574010450061)
        await user.add_roles(role)
        await user.remove_roles(role2)
        await channel.send(f'{member.name} reconheceu o Egresso')
        await reaction.message.delete()
        await asyncio.sleep(3)
        await channel.purge(limit=1)

        def enviar_email():  # função que envia o e-mail

            msg = email.message.Message()
            msg['Subject'] = "Autenticação"
            msg['From'] = 'bot.engenharia.computacao.ifpb@gmail.com'
            msg['To'] = email_egresso
            password = 'qhsrhphhvwsgbyxu'
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload('Você foi aceito no servidor oficial do curso de Engenharia de Computação - IFPB')

            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()
            # Login Credentials for sending the mail
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
            print('Email enviado')

        enviar_email()
        lista_espera_id = 1120674093159690310
        lista_espera = client.get_channel(lista_espera_id)
        await lista_espera.purge(limit=None)
        await lista_espera.send("Você foi aceito no servidor oficial do curso de Engenharia de Computação - IFPB")

    elif str(reaction.emoji) == '👎' and member.bot == False and canal == "coordenador_egressos":
        print("Não reconhecido")
        lista = client.get_channel(1120674093159690310)
        users = lista.members
        user = users[3]
        await user.guild.ban(user, reason='O usuário não foi reconhecido')
        await channel.send(f'{member.name} baniu o Usuário')
        await reaction.message.delete()
        await asyncio.sleep(3)
        await channel.purge(limit=1)

@client.event  # comando que vai-me permitir armazenar o endereço eletrónico informado pelo utilizador
async def on_message(message):
    mensagem = message.content
    canal = message.channel
    user = message.author
    print("%s em %s: %s "%(user,canal,mensagem))

    if "limpar" in message.content:
        await message.channel.purge(limit=None)
    tamanho = len(message.content)

    if "@" in message.content and "," not in message.content:
        global email_user
        response = message.content
        email_user = response
        nome = verificar_email(response, emails_alunos, nomes_alunos, emails_professores, nomes_professores)

        if nome!= None:  # aqui definimos que o nome do usuário vai ser igual o nome que consta na lista oficial
            await user.edit(nick=nome)

        elif email_user == "paulimskt1213@gmail.com":
            apelido = "<Dev_one>"
            await user.edit(nick=apelido)

        elif email_user == "marcosbelods@gmail.com":
            apelido = "<Dev_two>"
            await user.edit(nick=apelido)

        elif email_user == "henrique.cunha@ifpb.edu.br":
            apelido = "Coordenador"
            await user.edit(nick=apelido)

        if nome != None or email_user in listaD or email_user in listaC:
            global ident

            if response in emails_alunos or response in emails_professores or response in listaD or response in listaC:
                identificacao = random.randint(100000,
                                               999999)  # aqui eu estou gerarando uma senha de 6 digítos aleatória
                ident = str(identificacao)

                def enviar_email():  # função que envia o e-mail
                    ident

                    msg = email.message.Message()
                    msg['Subject'] = "Autenticação"
                    msg['From'] = 'bot.engenharia.computacao.ifpb@gmail.com'
                    msg['To'] = email_user
                    password = 'qhsrhphhvwsgbyxu'
                    msg.add_header('Content-Type', 'text/html')
                    msg.set_payload(ident)

                    s = smtplib.SMTP('smtp.gmail.com: 587')
                    s.starttls()
                    # Login Credentials for sending the mail
                    s.login(msg['From'], password)
                    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
                    print('Email enviado')

                enviar_email()

                await message.channel.send('Um e-mail contendo uma senha de 6 dígitos foi enviado, verifique e informe a senha em no máximo 5 minutos.')
                global inicio
                inicio = time.time()

        else:  # usuário é banido caso digite o e-mail errado
            await message.channel.send("Você será banido por informar o email incorreto.")
            guild = message.guild
            member = message.author
            await asyncio.sleep(3)
            await guild.ban(member, reason='E-mail informado está incorreto')
            await message.channel.purge(limit=None)

    if tamanho == 6 and "," not in message.content and message.content != "limpar":
        print("senha")
        passw = int(message.content)
        print(passw)
        fim = time.time()
        tempo = fim - inicio
        global cargo
        passowrd = passw

        if int(passowrd) == int(ident) and tempo < 360:
            cargo = True
            await message.channel.send('Senha verificada!')
            await message.channel.purge(limit=None)

            # nas linhas abaixo eu faço a atribuição dos cargos

            if email_user in emails_alunos and cargo:
                user = message.author
                role = user.guild.get_role(1116342141480869930)
                role2 = user.guild.get_role(1116342323975045231)
                await user.add_roles(role)
                await user.remove_roles(role2)

            elif email_user in emails_professores and cargo:
                user = message.author
                role = user.guild.get_role(1116341851348283442)
                role2 = user.guild.get_role(1116342323975045231)
                await user.add_roles(role)
                await user.remove_roles(role2)

            elif email_user in listaD and cargo:
                user = message.author
                role = user.guild.get_role(1116342085352693941)
                role2 = user.guild.get_role(1116342323975045231)
                await user.add_roles(role)
                await user.remove_roles(role2)

            elif email_user in listaC and cargo:
                user = message.author
                role = user.guild.get_role(1116341942687649803)
                role2 = user.guild.get_role(1116342323975045231)
                await user.add_roles(role)
                await user.remove_roles(role2)

        elif tempo > 360:
            await message.channel.send("Seu código de verificação expirou, repita o processo novamente.")

        else:  # usuário é banido caso digite a senha errada
            await message.channel.send("Você será banido por informar a senha incorreta.")
            guild = message.guild
            member = message.author
            await asyncio.sleep(3)
            await guild.ban(member, reason='Senha informada está incorreta')
            await message.channel.purge(limit=None)

    if "," in message.content and user.bot == False:
        data = datetime.datetime.now()
        data = str(data)
        ano = data[0:4]
        print("printar egresso")
        informacoes = message.content.split(",")

        if int(informacoes[1]) <= int(ano):
            global email_egresso
            email_egresso = str(informacoes[3])
            print(informacoes)
            user1 = message.author
            await user1.edit(nick=informacoes[0])
            await message.channel.purge(limit=None)
            embed = discord.Embed(title='Análise de identidade',description='O bot quer saber se pode permitir o seguinte usuário de entrar no servidor como "Egresso"', color=discord.Color.blue())
            embed.add_field(name= 'Usuário', value= message.author , inline=False)
            embed.add_field(name='Nome completo:', value= str(informacoes[0]) , inline=False)
            embed.add_field(name='Ano de conclusão:', value= str(informacoes[1]) , inline=False)
            embed.add_field(name='Data de nascimento:', value=str(informacoes[2]), inline=False)
            embed.add_field(name='E-mail de contato:', value=str(informacoes[3]), inline=False)

            channel_id = 1122861503595425852
            channel = client.get_channel(channel_id)
            message = await channel.send(embed=embed)

            await message.add_reaction('👍')
            await message.add_reaction('👎')

            role = user.guild.get_role(1120911574010450061)
            role2 = user.guild.get_role(1116342323975045231)

            lista_espera_id = 1120674093159690310
            await user.add_roles(role)
            await user.remove_roles(role2)
            lista_espera = client.get_channel(lista_espera_id)
            await lista_espera.send('Você foi adicionado a lista de espera, assim que for aceito receberá um e-mail informando.')

        else:
            await message.channel.send("Você será banido por fornecer informações incorretas.")
            guild = message.guild
            member = message.author
            await asyncio.sleep(3)
            await guild.ban(member, reason='Data de conclusão incorreta')
            await message.channel.purge(limit=None)

client.run("TOKEN")