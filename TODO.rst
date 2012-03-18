TODO
-----

* Sergio: Permitir que usuario atualize nome e sobrenome

* Jean: Pagina Reporte um problema
* Jean: Pagina Contribua

* Yure: Adicionar data do ultimo import de emails no footer
* Yure: Detectar links no conteudo e exibi-los como tal
* Yure: BUG: Display of HTML emails are wrong
* Arquivo "search.html" existente em "atu-colab/colab/templates" pode ser melhorado com relação ao conteúdo repetitivo dos "Tipos" exibidos no "Filtro" da página
* BUG: Criar validador de urls para twitter, facebook e página pessoal do user profile
* Mostrar dados do twitter, facebook, gtalk e página pessoal somente para os usuários que estiverem logados

* Configurar ADMINS no arquivo settings_local.py
* HTTPS para o trac, subversion e colab
* Autorizar usuarios a commitar no svn pelo django.contrib.admin
* Enviar emails para usuarios pedindo que se cadastrem no novo colab
* Timezones no trac/colab/solr nao estao compativeis

* Template de login nao exibe corretamente no firefox/linux
* Quando usuario se cadastra com email errado o email nunca eh validado, e o username fica preso 'pra sempre'.
* Nome dos usuarios errado nos emails que vem do Solr
* Adicionar ordering na busca
* Criar tipo usuario no solr
* Substituir sistema de cadastro por django-registration
* Utilizar pysolr para efetuar queries no Solr
* Melhorar buscas (case insensitive match, palavras com acentos)
* Indexar nome do repositorio como campo e exibi-lo no titulo dos changesets retornados
* Criacao de repositorios distribuidos pela interface do colab
* Link para última msg recebida na thread
* Fazer thread querysets ter um objeto (most_relevant_message)
* Implementar enviar email
* BUG: alguns subjects comecam e terminam com [] fazendo com que a RE de limpeza apague todo o subject.
* BUG: mensagens importadas por listas erradas
* Implementar login/signup usando LDAP
* Claime email address
* Merge emails dos usuarios
* Implementar badge system
* Melhorar filtros
* Link do thread preview deve enviar para mensagem da thread (anchor)
* Tornar todas as strings traduziveis
* Sugestão de como a divisão do edital seria melhor
* Indexar anexos da wiki (using Tika http://wiki.apache.org/solr/ExtractingRequestHandler)
* Filtrar usando calendario (como google analytics)
* Melhorar relevancia das buscas usando dismax queryparser
* Chat estilo Gmail usando o mensageiro Interlegis
* Sistema de gerencia de conteúdo
* Versao mobile
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
* Planet Interlegis (agregador de blogs)
* Filtros específicos para tipos diferentes na busca da thread
* Link para a mensagem original no histórico do Mailman (popup ajax)
* Filtro de mensagens nas listas acumulativos, podendo ligar e desligar todos
* Reduzir campos na tela de cadastro, transferindo-os como aba para a tela de profile, junto com a aba de listas a se inscrever)

* Indice criado manualmente. Automatizar:
  * create index super_archives_message_body_idx ON super_archives_message ((substring(body,0,1024)));
