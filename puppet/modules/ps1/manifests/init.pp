class ps1 (
  $color = 'red'
) {
  $color_code = $color ? {
    'red' => '1',
    'green' => '2',
    'yellow' => '3',
    default => '1'
  }

  $force_color_prompt_cmd = "/bin/sed -i -re '/force_color_prompt=yes/ s/^#//'"
  $force_color_prompt_condition = '/bin/grep "#force_color_prompt"'

  $ps1_color_cmd = "/bin/sed -i -re 's/01;3[1-3]m/01;3${color_code}m/'"
  $ps1_color_condition = "/bin/grep '01;3${color_code}m'"

  $skel_path = '/etc/skel/.bashrc'
  $root_path = '/root/.bashrc'

  # uncomment force_color_prompt in skel
  exec { "$force_color_prompt_cmd $skel_path":
    onlyif => "$force_color_prompt_condition $skel_path"
  }
  # uncomment  force_color_prompt in root
  exec { "$force_color_prompt_cmd $root_path":
    onlyif => "$force_color_prompt_condition $root_path"
  }

  # change prompt color in skel
  exec { "$ps1_color_cmd $skel_path":
    unless => "$ps1_color_condition $skel_path",
  }
  # change prompt color in root
  exec { "$ps1_color_cmd $root_path":
    unless => "$ps1_color_condition $root_path",
  }
}
