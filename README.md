* Para garantir que os teste das rotas fossem feitos no arquivo teste sem acessar o userModel, criei uma variavel de ambiente chamada Test. Para rodar os testes colocar essa variavel como true. Acredito que existe uma forma mais eficiente de fazer isso, mas por enquanto é o que deu pra fazer. 

* Para registrar o signup no csv, criei um método que verifica a existência do email no arquivo e dependendo da resposta, progredir com a escrita

* Para retornar a resposta sem a senha, usei um dict comprehension para selecionar apenas os campos desejados

* Para login, fiz um list comprehension que filtra todos os usuários no csv. Implementação bem parecida para deletar e atualizar os usúarios. Pega todos os usúarios, filtra e/ou altera com um list comprehension e sobreescreve a lista nova no arquivo antigo. 

* Para criar um novo id, acho o valor máximo de um lista extraida do csv.
