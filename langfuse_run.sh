docker run --name langfuse \
-e DATABASE_URL="postgresql://admin:root@host.docker.internal:5432/postgres" \
-e NEXTAUTH_URL=http://localhost:3000 \
-e NEXTAUTH_SECRET=mysecret \
-e SALT=mysalt \
-e ENCRYPTION_KEY=0000000000000000000000000000000000000000000000000000000000000000 \
-p 3000:3000 \
langfuse/langfuse
