#===========================================================================#
#Description: Deploy azure resource using ARM templates
#Author: Ramya Balusamy
#Date: 07/28/2019
#===========================================================================#

param(

[Parameter(Mandatory=$True)]
 [string]
 $subscriptionId,

 [Parameter(Mandatory=$True)]
 [string]
 $resourceGroupName,

 [string]
 $resourceGroupLocation,

 [string]
 $tenantid,

 [string]
 $applicationId,

 [string]
 $applicationkey,

 [Parameter(Mandatory=$True)]
 [string]
 $deploymentName,

 [string]
 $templateFilePath = "template.json",

 [string]
 $parametersFilePath = "parameters.json"

)

$ErrorActionPreference = "stop"

Try{

#Authentication

$securePassword = $applicationkey | ConvertTo-SecureString -AsPlainText -Force

$credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $applicationId, $securePassword

Connect-AzureRmAccount -ServicePrincipal -Credential $credential -Subscription $subscriptionId -TenantId $tenantid

function Deploy-Resources($deploymentName, $resourceGroupName, $templateFilePath, $parametersFilePath){

New-AzureRmResourceGroupDeployment -Name $deploymentName -ResourceGroupName $resourceGroupName -TemplateFile $templateFilePath -TemplateParameterFile $parametersFilePath -Force

}

Deploy-Resources $deploymentName $resourceGroupName $templateFilePath $parametersFilePath

}

Catch{

$ErrorMessage = $_.Exception.Message

$ErrorMessage

}