# Coleta de Informações de Hardware e IP Externo

Write-Host "==== Informações da Máquina ===="

# UUID da Baseboard
$uuid = (Get-WmiObject Win32_ComputerSystemProduct).UUID
Write-Host "UUID Baseboard: $uuid"

# Serial da Baseboard
$baseboardSerial = (Get-WmiObject Win32_BaseBoard).SerialNumber
Write-Host "Serial Baseboard: $baseboardSerial"

# Volume ID (C:)
$volumeID = (Get-WmiObject Win32_LogicalDisk | Where-Object { $_.DeviceID -eq 'C:' }).VolumeSerialNumber
Write-Host "Volume ID (C:): $volumeID"

# Serial do Disco
$diskSerial = (Get-WmiObject Win32_PhysicalMedia | Select-Object -ExpandProperty SerialNumber)[0]
Write-Host "Disk Serial: $diskSerial"

# MAC Address
$macAddresses = Get-WmiObject Win32_NetworkAdapterConfiguration | Where-Object { $_.MACAddress -ne $null } | Select-Object -ExpandProperty MACAddress
Write-Host "MAC Addresses:"
$macAddresses | ForEach-Object { Write-Host " - $_" }

# IP Externo
try {
    $ipExterno = (Invoke-WebRequest -Uri "https://api.ipify.org").Content
    Write-Host "IP Externo: $ipExterno"
} catch {
    Write-Host "IP Externo: Falha ao obter (verifique sua conexão com a internet)"
}

# Serial do Monitor (Pode não funcionar em todos os sistemas)
try {
    $monitorSerial = (Get-WmiObject WmiMonitorID -Namespace root\wmi | ForEach-Object {
        ($_.SerialNumberID | ForEach-Object { [char]$_ }) -join ''
    })
    if ($monitorSerial) {
        Write-Host "Monitor Serial: $monitorSerial"
    } else {
        Write-Host "Monitor Serial: Não encontrado ou não suportado."
    }
} catch {
    Write-Host "Monitor Serial: Falha ao tentar obter."
}

Write-Host "==== Fim da coleta ===="

# Mantém a janela aberta
Read-Host "Pressione Enter para sair"
