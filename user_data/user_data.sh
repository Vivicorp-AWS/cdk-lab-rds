#!/bin/bash
cat > /home/ssm-user/hello_world.sh << EOF
echo "Hello World!"
EOF

chmod +x /home/ssm-user/hello_world.sh
