
include supervisor

supervisor::app { 'fake_service': 
  command => '/bin/cat',
  directory => '/tmp/', 
}
