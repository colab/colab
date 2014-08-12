#Instalação do Solr 4.6.1
#------------------------

## Atualizacao
sudo yum update -y

##Instalacao das Dependencias
sudo yum install -y wget java-1.7.0-openjdk vim

## 0. Libere a porta 8983 desta máquina para que máquina do colab possa ouvi-la
#sudo iptables -A INPUT -p tcp -dport 8983 -j ACCEPT
#sudo /sbin/service iptables save

##Faça o download e descompacte o Solr no /tmp
sudo wget http://archive.apache.org/dist/lucene/solr/4.6.1/solr-4.6.1.tgz -O /tmp/solr-4.6.1.tgz
sudo tar xvzf /tmp/solr-4.6.1.tgz -C /usr/share
sudo mv /usr/share/solr-4.6.1 /usr/share/solr

#Instale o Solr no diretório ``/usr/share``
sudo cp /usr/share/solr/example/webapps/solr.war /usr/share/solr/example/solr/solr.war

#Remova a tag ``updateLog`` no solrconfig.xml
sudo wget https://gitlab.com/softwarepublico/colabdocumentation/raw/master/Arquivos/solr/solrconfig.xml -O /usr/share/solr/example/solr/collection1/conf/solrconfig.xml

#Copiar o solr schema
sudo wget https://gitlab.com/softwarepublico/colabdocumentation/raw/master/Arquivos/solr/schema.xml -O /usr/share/solr/example/solr/collection1/conf/schema.xml

#Copiar script de inicialização
sudo wget https://gitlab.com/softwarepublico/colabdocumentation/raw/master/Arquivos/solr/solrinit -O /etc/init.d/solr
sudo chmod +x /etc/init.d/solr

sudo wget https://gitlab.com/softwarepublico/colabdocumentation/raw/master/Arquivos/solr/start.sh -O /usr/share/solr/start.sh
sudo chmod +x /usr/share/solr/start.sh

sudo chkconfig solr on

#Inicie o solr
sudo service solr start