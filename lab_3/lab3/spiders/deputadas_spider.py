import scrapy
from scrapy.selector import Selector
import csv
import os

# lista_deputadas = []
meses = {
    "Janeiro/2022": "gasto_jan_par",
    "Fevereiro/2022": "gasto_fev_par",
    "Março/2022": "gasto_mar_par",
    "Abril/2022": "gasto_abr_par",
    "Maio/2022": "gasto_maio_par",
    "Junho/2022": "gasto_junho_par",
    "Julho/2022": "gasto_jul_par",
    "Agosto/2022": "gasto_agosto_par",
    "Setembro/2022": "gasto_set_par",
    "Outubro/2022": "gasto_out_par"
}

deputadas = {}
file = open('deputadas_e_deputados.csv', 'a')
writer = csv.writer(file)
if os.stat("deputadas_e_deputados.csv").st_size == 0:
    writer.writerow(['nome', 'genero', 'data_nascimento', 'salario_bruto', 'quant_viagem', 'presença_plenario', 'ausencia_plenario',
    'ausencia_justificada_plenario', 'presenca_comissao', 'ausencia_comissao',
    'ausencia_justificada_comissao', 'gasto_total_par',
    'gasto_jan_par', 'gasto_fev_par', 'gasto_mar_par', 'gasto_abr_par' , 'gasto_maio_par',
    'gasto_junho_par', 'gasto_jul_par', 'gasto_agosto_par', 'gasto_set_par',
    'gasto_out_par', 'gasto_nov_par', 'gasto_dez_par',
    'gasto_jan_gab', 'gasto_fev_gab', 'gasto_mar_gab', 'gasto_abr_gab' ,
    'gasto_maio_gab', 'gasto_junho_gab', 'gasto_jul_gab', 'gasto_agosto_gab',
    'gasto_set_gab', 'gasto_out_gab', 'gasto_nov_gab', 'gasto_dez_gab'])

file.close()

class DeputadasSpider(scrapy.Spider):
    name = "deputadas"

    def start_requests(self):
        file = open("lista_deputadas.txt")
        string = file.read()
        lista_urls = string.split('\n')

        # lista_urls = ['https://www.camara.leg.br/deputados/204528']

        for url in lista_urls:
            if (url != ''):
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
               
        # filename = f'links_deputadas.html'
        # dep =  response.css('h3.lista-resultados__cabecalho').getall()
        try:
            nome = response.css('.informacoes-deputado > li:first-child::text').get().strip()
            email = response.css('.informacoes-deputado > li:nth-child(2) > a::text').get()
            genero = 'F'
            data_nascimento = response.css('.informacoes-deputado > li:nth-child(5)::text').get().strip()
            presenca_plenario = response.css('.atuacao-deputado > div.list-table > ul.list-table__content > li.list-table__item:nth-child(1) > dl.list-table__definition-list > dd.list-table__definition-description:nth-child(2)::text').get().replace('\n', '').strip()
            ausencia_just_plenario = response.css('.atuacao-deputado > div.list-table > ul.list-table__content > li.list-table__item:nth-child(1) > dl.list-table__definition-list > dd.list-table__definition-description:nth-child(4)::text').get().replace('\n', '').strip()
            ausencia_nao_just_plenario = response.css('.atuacao-deputado > div.list-table > ul.list-table__content > li.list-table__item:nth-child(1) > dl.list-table__definition-list > dd.list-table__definition-description:nth-child(6)::text').get().replace('\n', '').strip()
            presenca_comissoes = response.css('.atuacao-deputado > div.list-table > ul.list-table__content > li.list-table__item:nth-child(2) > dl.list-table__definition-list > dd.list-table__definition-description:nth-child(2)::text').get().replace('\n', '').strip()
            ausencia_just_comissoes = response.css('.atuacao-deputado > div.list-table > ul.list-table__content > li.list-table__item:nth-child(2) > dl.list-table__definition-list > dd.list-table__definition-description:nth-child(4)::text').get().replace('\n', '').strip()
            ausencia_nao_just_comissoes = response.css('.atuacao-deputado > div.list-table > ul.list-table__content > li.list-table__item:nth-child(2) > dl.list-table__definition-list > dd.list-table__definition-description:nth-child(6)::text').get().replace('\n', '').strip()
            salario_bruto = response.css('ul.recursos-beneficios-deputado-container > li:nth-child(2) > div.beneficio > a.beneficio__info::text').get().strip()
            quant_viagem = response.css('ul.recursos-beneficios-deputado-container > li:nth-child(5) > div.beneficio__viagens > span.beneficio__info::text').get().strip()
            link_gastos_par = response.css('li.gasto:nth-child(1) > .veja-mais > a').attrib['href']
            link_gastos_gab = response.css('li.gasto:nth-child(2) > .veja-mais > a').attrib['href']

            #gastos_meses_parlamentar = response.css("table[id=gastomensalcotaparlamentar]>tbody>tr>td::text").getall()
            #gastos_meses_gabinete = response.css("table[id=gastomensalverbagabinete]>tbody>tr>td::text").getall()
            #gastos_meses_par_limpo = []
            #gastos_meses_gab_limpo = []

            #for i in range(len(gastos_meses_parlamentar)):
            #if (i % 2 == 0):
            #    gastos_meses_par_limpo.append(gastos_meses_parlamentar[i])

        except:
            return

        # for i in dep:
        #     body = i
        #     aux = Selector(text=body).xpath('//a/@href').get()
        #     print(aux)
        #     lista_deputadas.append(aux)

        # Salva os links em txt
        # file=open('lista_deputadas.txt','w')
        # header = ['nome', 'genero', 'data_nascimento', 'presença_plenario', 'ausencia_plenario', 'ausencia_justificada_plenario', 'presenca_comissao', 'ausencia_comissao', 'ausencia_justificada_comissao']
        data = [nome, genero, data_nascimento, salario_bruto, quant_viagem, presenca_plenario, ausencia_nao_just_plenario, ausencia_just_plenario, presenca_comissoes, ausencia_nao_just_comissoes, ausencia_just_comissoes]
        deputadas[email] = data

        yield response.follow(link_gastos_par, callback=lambda r: self.parse_gastos_par(response=r, email=email, link_gastos_gab=link_gastos_gab))
    
    def parse_gastos_par(self, response, email, link_gastos_gab):
        gasto_total_par = response.css('tbody > tr.mestre > td::text').get().strip()

        gastos_meses_init = {
            "Janeiro/2022": None,
            "Fevereiro/2022": None,
            "Março/2022": None,
            "Abril/2022": None,
            "Maio/2022": None,
            "Junho/2022": None,
            "Julho/2022": None,
            "Agosto/2022": None,
            "Setembro/2022": None,
            "Outubro/2022": None,
            "Novembro/2022": None,
            "Dezembro/2022": None
        }
        gastos_meses = response.css('tbody > tr.detalhe').getall()
        for i in range(len(gastos_meses)):
            mes = response.css("tbody > tr.detalhe:nth-child({index}) > th:nth-last-child(2) > a::text".format(index=i+2)).get().strip()
            if mes in gastos_meses_init.keys():
                gastos_meses_init[mes] = response.css('tbody > tr.detalhe:nth-child({index}) > td::text'.format(index=i+2)).get().strip()

        gastos = gastos_meses_init.values()
        deputadas[email].append(gasto_total_par)
        deputadas[email].extend(gastos)

        yield response.follow(link_gastos_gab, callback=lambda r: self.parse_gastos_gab(response=r, email=email))
    
    def parse_gastos_gab(self, response, email):
        # gasto_total_par = response.css('tbody > tr.mestre > td::text').get().strip()

        gastos_meses_init = {
            "01": None,
            "02": None,
            "03": None,
            "04": None,
            "05": None,
            "06": None,
            "07": None,
            "08": None,
            "09": None,
            "10": None,
            "11": None,
            "12": None
        }
        gastos_meses = response.css('tbody > tr').getall()
        for i in range(len(gastos_meses)):
            mes = response.css("tbody > tr:nth-child({index}) > td:first-child::text".format(index=i+1)).get().strip()
            if mes in gastos_meses_init.keys():
                gastos_meses_init[mes] = response.css("tbody > tr:nth-child({index}) > td:nth-child(3)::text".format(index=i+1)).get().strip()

        gastos = gastos_meses_init.values()
        deputadas[email].extend(gastos)

        with open('deputadas_deputados.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(deputadas[email])