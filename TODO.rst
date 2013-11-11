TODO
-----

Emails
=======
* Atualizar versão do Mailman
* Sincronizar informações de  membership do mailman com o django
* Usar informações do banco de dados local ao inves de fazer queries constantes
* Logar erros ao falhar inscricao ou remocao de listas
* Processo de cadastro em listas com moderacao
* Permitir moderacao de mensagens pelo Colab
* Permitir a gestao de listas pelo Colab
* Não perder o email em caso de falha de envio. Exibir o erro mas trazer a mensagem de volta para o usuário
* Permitir apenas que usuarios pertencentes a lista enviem mensagens 


Updates
======
* Atualizar a versao do Django para 1.7
* Remover South (django 1.7 ja implementa migrations)


Async
=====
* Usar celery para tornar tasks como envio de emails asincronas.


Planet
======

* Paginator esta quebrado em telas xs


Chat
====

* Permitir que usuario altere senha


Interface
=========

* Utilizar paginador do bootstrap 3 em todas as telas
* Implementar breadcrumbs
* Utilizar biblioteca de gráficos local (substituir google charts)
* Melhorar filtros para interfaces móveis
* Paginar discussoes
* Paginar dashboard de discussoes
* Highlight mostrar resultados normalizados (com e sem acentos)
* Adicionar opção para escolha de idioma


Outros
=======

* Contabilizar votos dentro do modelo de mensagem. Com a implementação atual ordenar uma thread por votos é uma operação muito cara.
* Utilizar SOLR para listar documentos relevantes ao inves de thread.score
* Escrever casos de teste
* Criacao de repositorios distribuidos pela interface do colab
* Fazer thread querysets ter um objeto (most_relevant_message)
* BUG: alguns subjects comecam e terminam com [] fazendo com que a RE de limpeza apague todo o subject.
* BUG: mensagens importadas por listas erradas
* Migração e reorganização do conteúdo do trac/wiki para o novo colab
* Indice criado manualmente. Automatizar:
  * create index super_archives_message_body_idx ON super_archives_message ((substring(body,0,1024)));
