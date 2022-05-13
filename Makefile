#terraform -chdir=aws/infra/cluster/bastion/ apply -auto-approve

#terraform -chdir=aws/infra/network/ init
#terraform -chdir=aws/infra/s3/ apply
SINGLE := cluster/master cluster/slave  	 # order apply
REV_SINGLE := cluster/slave cluster/master #cluster/bastion network 	 # order destroy



infra/apply:
	# Apply cluster
	for i in  $(SINGLE); do \
		terraform -chdir=aws/infra/$$i apply -auto-approve ; \
	done
	@echo "[Apply cluster] OK"

infra/destroy:
	# Destroy cluster
	for i in  $(REV_SINGLE); do \
		terraform -chdir=aws/infra/$$i destroy -auto-approve ; \
	done
	@echo "[Destroy cluster] OK"
