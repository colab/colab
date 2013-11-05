TODO
-----

Async
=====
* Usar celery para tornar tasks como envio de emails asincronas.


Envio de emails
===============
* Não perder o email em caso de falha de envio. Exibir o erro mas trazer a mensagem de volta para o usuário
* Permitir apenas que usuarios pertencentes a lista enviem mensagens 


Planet
======

* Paginator esta quebrado em telas xs

Chat
====

* Allow user to change passwords


Outros
=======

* Adicionar data do ultimo import de emails no footer
* Detectar links no conteudo e exibi-los como tal
* BUG: Display of HTML emails are wrong
* Arquivo "search.html" existente em "atu-colab/colab/templates" pode ser melhorado com relação ao conteúdo repetitivo dos "Tipos" exibidos no "Filtro" da página
* BUG: Criar validador de urls para twitter, facebook e página pessoal do user profile
* Mostrar dados do twitter, facebook, gtalk e página pessoal somente para os usuários que estiverem logados
* Configurar ADMINS no arquivo settings_local.py
* HTTPS para o trac, subversion e colab

* Quando usuario se cadastra com email errado o email nunca eh validado, e o username fica preso 'pra sempre'.
* Nome dos usuarios errado nos emails que vem do Solr
* Adicionar ordering na busca
* Criar tipo usuario no solr
* Utilizar haystack 
* Melhorar buscas (case insensitive match, palavras com acentos)
* Indexar nome do repositorio como campo e exibi-lo no titulo dos changesets retornados
* Criacao de repositorios distribuidos pela interface do colab
* Link para última msg recebida na thread
* Fazer thread querysets ter um objeto (most_relevant_message)
* Implementar enviar email
* BUG: alguns subjects comecam e terminam com [] fazendo com que a RE de limpeza apague todo o subject.
* BUG: mensagens importadas por listas erradas
* Claime email address
* Merge emails dos usuarios
* Implementar badge system
* Melhorar filtros
* Link do thread preview deve enviar para mensagem da thread (anchor)
* Indexar anexos da wiki (using Tika http://wiki.apache.org/solr/ExtractingRequestHandler)
* Filtrar usando calendario (como google analytics)
* Melhorar relevancia das buscas usando dismax queryparser
* Exibir discussões relacionadas na barra da direita das discussões
* Migração e reorganização do conteúdo do trac/wiki para o novo colab
* Ao importar mensagem sem subject enviar email avisando o usuario que ele esta enviando um email sem o campos "Assunto"
* Remover ou ocultar trechos da mensagem que iniciem com ">" assim como o Gmail.
* Contar page views no trac (ticket, wiki e changeset) e utiliza-los para rankear paginas nas buscas
* Mostrar highlight nas buscas
* Sistema de tags para as mensagens
* Tag cloud para as mensagens, ao lado direito da thread
* Pagina home para cada lista com os mesmo filtros da home atual
* Permitir que usuario entre e saia de listas ao editar perfil
* Filtros específicos para tipos diferentes na busca da thread
* Link para a mensagem original no histórico do Mailman (popup ajax)
* Filtro de mensagens nas listas acumulativos, podendo ligar e desligar todos
* Indice criado manualmente. Automatizar:
  * create index super_archives_message_body_idx ON super_archives_message ((substring(body,0,1024)));
